<template>
  <v-card id="map-container">
    <!-- MAP PLOT -->
    <v-container fluid fill-height>
      <v-row ref="plotContainer" justify="center">
        <svg id="svg" ref="svg"></svg>
      </v-row>
    </v-container>

    <!-- SPEED DIAL -->
    <v-speed-dial
      bottom
      right
      v-model="backgroundFABActive"
      direction="top"
      transition="slide-y-reverse-transition"
    >
      <template v-slot:activator>
        <v-btn light fab v-model="backgroundFABActive">
          <v-icon v-if="backgroundFABActive">{{ icons.mdiClose }}</v-icon>
          <v-icon v-else>{{ icons.mdiMap }}</v-icon>
        </v-btn>
      </template>
      <v-card light>
        <v-container light fluid>
          <v-list light dense>
            <v-list-item-group v-model="backgroundIndex">
              <v-list-item
                class="list-item-rounded"
                v-for="(item, i) in backgrounds"
                :key="i"
                @click="background = item"
              >
                <v-list-item-content>
                  <v-list-item-title v-text="item"></v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-container>
      </v-card>
    </v-speed-dial>
  </v-card>
</template>

<script>
import {
  select,
  selectAll,
  path,
  drag,
  scaleLinear,
  axisTop,
  axisLeft,
  axisRight,
} from "d3";
import cloneDeep from "lodash/cloneDeep";
import { mdiClose, mdiMap } from "@mdi/js";

/**
 * Haversine formula. Generally used geo measurement function.
 * See: https://www.movable-type.co.uk/scripts/latlong.html
 */
function getHaversineDist(lat1, lon1, lat2, lon2) {
  const R = 6378.137; // Earth's radius, in kilometers
  const phi1 = (lat1 * Math.PI) / 180; // phi, lambda in radians
  const phi2 = (lat2 * Math.PI) / 180;
  const dPhi = ((lat2 - lat1) * Math.PI) / 180;
  const dLambda = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dPhi / 2) * Math.sin(dPhi / 2) +
    Math.cos(phi1) *
      Math.cos(phi2) *
      Math.sin(dLambda / 2) *
      Math.sin(dLambda / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const d = R * c; // kilometers
  return d * 100000; // centimetres
}

export default {
  name: "MapView",

  props: {
    cruiseName: {
      type: String,
      default: () => "",
    },
    cruiseData: {
      type: Array,
      default: () => [],
    },
    backgrounds: {
      type: Array,
      default: () => [],
    },
    site: {
      type: String,
      default: () => "",
    },
    startDate: {
      type: Date,
      default: () => new Date(),
    },
    endDate: {
      type: Date,
      default: () => new Date(),
    },
    fates: {
      type: Array,
      default: () => [],
    },
    dragColor: {
      type: String,
      default: () => "",
    },
    dragMode: {
      type: String,
      default: () => "",
    },
    newSelectedCylinders: {
      type: Array,
      default: () => [],
    },
  },

  data: () => ({
    publicPath: process.env.BASE_URL,
    icons: {
      mdiClose: mdiClose,
      mdiMap: mdiMap,
    },

    // plot variables
    svgWidth: undefined,
    svgHeight: undefined,
    plotMargins: undefined,
    plotWidth: undefined,
    plotHeight: undefined,
    xScale: undefined,
    yScale: undefined,
    xAxis: undefined,
    yAxis: undefined,
    svg: undefined,
    plotGroup: undefined,
    bgGroup: undefined,
    xAxisGroup: undefined,
    yAxisGroup: undefined,
    xGridlinesGroup: undefined,
    yGridlinesGroup: undefined,
    dragGroup: undefined,
    marksGroup: undefined,

    // settings
    dragElement: null,
    dragBehavior: null,
    background: "None",
    backgroundIndex: 0,
    background_data: undefined,
    filter: undefined,

    // data
    cylinders: {
      all: [],
      selected: [],
      selection: {
        allowed: true,
        border: {
          show: true,
          exists: false,
        },
      },
    },
    xVar: "Longitude",
    yVar: "Latitude",

    // flags
    backgroundFABActive: false,
  }),

  mounted: function () {
    let vm = this;
    vm.svg = select("#svg"); // get svg once mounted

    // refresh the svg on resize
    window.addEventListener("resize", () => {
      vm.init();
      if (vm.background && vm.background !== "None") {
        vm.loadBackgroundData().then(vm.draw);
      } else {
        vm.draw();
      }
    });

    // define how to create a drag element
    vm.dragElement = {
      id: 0,
      context: null,
      previousContext: null,
      element: null,
      elementStack: [],
      elementIDStack: [],
      container: null, // will be set in init
      currentY: 0,
      currentX: 0,
      originX: 0,
      originY: 0,
      init: function (newX, newY) {
        let element, context;
        switch (vm.dragMode) {
          case "Draw":
            context = path();
            context.moveTo(newX, newY);
            this.setContext(context);
            element = this.container
              .append("path")
              .classed(`drag-path-${this.id}`, true)
              .attr("stroke", vm.dragColor)
              .attr("stroke-width", "2px")
              .attr("stroke-opacity", "1")
              .attr("fill", "none");
            break;
          case "Select":
          case "Zoom":
            element = this.container
              .append("rect")
              .classed("drag-rect", true)
              .attr("x", 0)
              .attr("y", 0)
              .attr("width", 0)
              .attr("height", 0)
              .attr("rx", 4)
              .attr("ry", 4)
              .attr("stroke", "#545454")
              .attr("stroke-width", "2px")
              .attr("stroke-opacity", "1")
              .attr("fill", "white")
              .attr("fill-opacity", "0.5");
            break;
        }
        this.setElement(element);
        this.originX = newX;
        this.originY = newY;
        this.update(newX, newY);
      },
      update: function (evtX, evtY) {
        switch (vm.dragMode) {
          case "Draw":
            if (
              evtX >= 0 &&
              evtX <= vm.plotWidth &&
              evtY >= 0 &&
              evtY <= vm.plotHeight
            ) {
              // inside the boundary
              if (this.element) {
                // path is currently being drawn, continue
                this.currentX = evtX;
                this.currentY = evtY;
                this.context.lineTo(this.currentX, this.currentY);
                this.element.attr("d", this.context); // draw the line
              } else {
                // no path yet, make a new one and start drawing
                this.init(evtX, evtY);
              }
            } else {
              // outside the boundary, stop
              if (this.element) {
                // unset the path element reference to stop drawing to it
                this.setElement(null);
              }
            }
            break;
          case "Select":
          case "Zoom": {
            if (this.element) {
              // adjust x,y to stick to the boundaries
              let newX =
                evtX < 0 ? 0 : evtX > vm.plotWidth ? vm.plotWidth : evtX;
              let newY =
                evtY < 0 ? 0 : evtY > vm.plotHeight ? vm.plotHeight : evtY;
              this.currentX = newX;
              this.currentY = newY;
              // allow the selection rect to be drawn opposite the origin
              const x =
                this.currentX < this.originX ? this.currentX : this.originX;
              const y =
                this.currentY < this.originY ? this.currentY : this.originY;
              const rectWidth = Math.abs(this.currentX - this.originX);
              const rectHeight = Math.abs(this.currentY - this.originY);
              this.element
                .attr("x", x)
                .attr("y", y)
                .attr("width", rectWidth)
                .attr("height", rectHeight);
              break;
            }
          }
        }
      },
      setContext: function (ctx) {
        this.previousContext = this.context;
        this.context = ctx;
      },
      setElement: function (ele) {
        this.element = ele;
      },
      removeElement: function () {
        this.element.remove();
        this.element = null;
      },
      incrementElementID: function () {
        this.id++;
      },
      pushCurrentElementToStack: function () {
        this.elementIDStack.push(this.id);
        this.elementStack.push(this.element.node().cloneNode(true));
      },
      popElementFromStack: function () {
        return [this.elementIDStack.pop(), this.elementStack.pop()];
      },
      drawElementsInStack: function () {
        this.elementStack.forEach((elem) =>
          this.container.node().appendChild(elem)
        );
      },
      getCurrentAttributes: function () {
        const x = +this.element.attr("x");
        const y = +this.element.attr("y");
        switch (vm.dragMode) {
          case "Draw":
            return {
              x: x,
              y: y,
            };
          case "Select":
          case "Zoom": {
            const rectWidth = +this.element.attr("width");
            const rectHeight = +this.element.attr("height");
            return {
              x1: x,
              y1: y,
              x2: x + rectWidth,
              y2: y + rectHeight,
            };
          }
        }
      },
    };

    let dragStart = (e) => {
      vm.dragElement.init(e.x, e.y);
    };

    let dragMove = (e) => {
      vm.dragElement.update(e.x, e.y);
    };

    let dragEnd = () => {
      // take action based on the current drag mode
      switch (vm.dragMode) {
        case "Draw":
          vm.dragElement.pushCurrentElementToStack();
          vm.dragElement.incrementElementID();
          break;
        case "Select":
        case "Zoom": {
          let attrs = vm.dragElement.getCurrentAttributes();
          vm.dragElement.removeElement();
          if (attrs.x2 - attrs.x1 > 1 && attrs.y2 - attrs.y1 > 1) {
            // large enough drag region was made, attempt action
            const xMin = vm.xScale.invert(attrs.x1);
            const xMax = vm.xScale.invert(attrs.x2);
            const yMin = vm.yScale.invert(attrs.y2);
            const yMax = vm.yScale.invert(attrs.y1);
            switch (vm.dragMode) {
              case "Zoom":
                vm.filter.stack.push(cloneDeep(vm.filter)); // push the prior filter values onto the filter stack
                vm.setXYFilter(xMin, xMax, yMin, yMax); // update filter values
                vm.squareFilters(); // apply transformations to the filters
                break;
              case "Select":
                // filter list of data points
                vm.cylinders.selected = vm.cylinders.all
                  .filter((p) => {
                    return (
                      p.xVar >= xMin &&
                      p.xVar <= xMax &&
                      p.yVar >= yMin &&
                      p.yVar <= yMax
                    );
                  })
                  .map((p) => p.Cylinder);
                vm.$emit("updateSelectedCylinders", vm.cylinders.selected);
                // reset drag mode to zoom by default
                vm.$emit("updateDragMode", "Zoom");
                break;
            }
          }
          vm.draw(); // re-draw the vis
          break;
        }
      }
    };

    // create function to call
    vm.dragBehavior = drag()
      .on("start", dragStart)
      .on("drag", dragMove)
      .on("end", dragEnd);

    // start the show!
    if (vm.cruiseData.length > 0) {
      vm.init();
      vm.parseData(vm.cruiseData);
      vm.filterBySite();
      if (vm.background && vm.background !== "None") {
        vm.loadBackgroundData().then(vm.draw);
      } else {
        vm.draw();
      }
    }
  },

  watch: {
    cruiseData: function (newData) {
      let vm = this;
      vm.background = "None"; // make sure no background loads
      vm.backgroundIndex = 0; // reset selected background
      vm.init();
      vm.parseData(newData);
      vm.draw();
    },

    newSelectedCylinders: function (newCylinders) {
      let vm = this;
      // only update selected list if incoming list is different from current selection
      const cylindersSorted = vm.cylinders.selected.slice().sort();
      const newCylindersSorted = newCylinders.slice().sort();
      const same =
        cylindersSorted.length === newCylindersSorted.length &&
        cylindersSorted.every(function (value, index) {
          return value === newCylindersSorted[index];
        });
      if (!same) {
        vm.cylinders.selected = newCylinders;
      }
      vm.draw();
    },

    background: function () {
      let vm = this;
      vm.init();
      if (vm.background && vm.background !== "None") {
        vm.loadBackgroundData().then(vm.draw);
      } else {
        vm.draw();
      }
    },

    site: function () {
      let vm = this;
      vm.filterBySite();
      vm.draw();
    },

    startDate: function () {
      let vm = this;
      vm.draw();
    },

    endDate: function () {
      let vm = this;
      vm.draw();
    },

    fates: function () {
      let vm = this;
      vm.draw();
    },
  },

  methods: {
    init() {
      let vm = this;

      // define background image files
      const path = `${vm.publicPath}assets/backgrounds/${vm.cruiseName}/${vm.background}`;
      vm.background_data = {
        meta: undefined,
        tif: `${path}.tif`,
        png: `${path}.png`,
        json: `${path}.json`,
      };

      // set the svg width and height based on the container
      const containerWidth = this.$refs.plotContainer.clientWidth;
      const containerHeight = window.innerHeight - 176; // -176px app-bar
      vm.svgWidth = containerWidth;
      vm.svgHeight = containerHeight;
      // vm.svgWidth = Math.min(containerWidth, containerHeight);
      // vm.svgHeight = Math.min(containerWidth, containerHeight);

      // set plot margins, width and height
      vm.plotMargins = { top: 44, bottom: 2, left: 44, right: 2 };
      vm.plotWidth = vm.svgWidth - vm.plotMargins.left - vm.plotMargins.right;
      vm.plotHeight = vm.svgHeight - vm.plotMargins.top - vm.plotMargins.bottom;

      // update svg
      vm.svg.selectAll("*").remove(); // clear out any objects already in the svg
      vm.svg.attr("width", vm.svgWidth).attr("height", vm.svgHeight);

      // Add plot group, containing axes, marks, and legend
      vm.plotGroup = vm.svg
        .append("g")
        .classed("plot", true)
        .attr(
          "transform",
          `translate(${vm.plotMargins.left},${vm.plotMargins.top})`
        );

      // add background group
      vm.bgGroup = vm.plotGroup.append("g").classed("bg", true);

      // add svg to the background group to occlude oversized children
      vm.bgGroup
        .append("svg")
        .attr("width", vm.plotWidth)
        .attr("height", vm.plotHeight);

      // if a background is selected, add it to the background svg
      if (vm.background && vm.background !== "None") {
        vm.bgGroup
          .select("svg")
          .append("svg:image")
          .attr("preserveAspectRatio", "none")
          .attr("xlink:href", vm.background_data.png);
      }

      // Add X and Y axis groups
      vm.yAxisGroup = vm.plotGroup
        .append("g")
        .classed("y", true)
        .classed("axis", true);
      vm.xAxisGroup = vm.plotGroup
        .append("g")
        .classed("x", true)
        .classed("axis", true);
      // .attr("transform", `translate(${0},${vm.plotHeight})`);

      // add gridlines groups
      vm.xGridlinesGroup = vm.plotGroup
        .append("g")
        .classed("x-gridlines", true);
      vm.yGridlinesGroup = vm.plotGroup
        .append("g")
        .classed("y-gridlines", true);

      // Add data marks group
      vm.marksGroup = vm.plotGroup.append("g").classed("marks", true);

      // add svg to the marks group for the selection outline
      vm.marksGroup
        .append("svg")
        .attr("id", "selection-border-container")
        .attr("width", vm.plotWidth)
        .attr("height", vm.plotHeight);

      // Add drag group to the marks group, over the selection container
      vm.dragGroup = vm.marksGroup.append("g").classed("drag", true);

      // plot the dragElement and stored elements
      vm.dragElement.container = vm.dragGroup;
      vm.dragElement.drawElementsInStack();

      // add selection region to drag group
      vm.dragGroup
        .append("rect")
        .attr("width", vm.plotWidth)
        .attr("height", vm.plotHeight)
        .style("opacity", 0)
        .call(vm.dragBehavior);
    },

    parseData(newData) {
      let vm = this;

      // create list of data points with only id columns
      const rawCylinderList = newData.map((p) => {
        return {
          Cylinder: p["Cylinder"],
          Location: p["Location"],
          Type: p["Core Fate"],
          Date: p["Date"],
          xVar: parseFloat(p[vm.xVar]),
          yVar: parseFloat(p[vm.yVar]),
        };
      });

      // remove duplicate data points by Cylinder name (keep the last one found)
      vm.cylinders.all = [
        ...new Map(
          rawCylinderList.map((item) => [item["Cylinder"], item])
        ).values(),
      ];

      // set filter object to initial values
      vm.filter = {
        x: [0, 100],
        y: [0, 100],
        dx: 100,
        dy: 100,
        stack: [],
        extent: {
          x: [0, 100],
          y: [0, 100],
        },
        hav_dist: {
          x: {
            y_min: 100,
            y_max: 100,
          },
          y: 100,
        },
      };

      // set initial filter to first point
      let p = vm.cylinders.all[0];
      let xMin = p.xVar;
      let xMax = p.xVar;
      let yMin = p.yVar;
      let yMax = p.yVar;

      // collect points
      for (let i = 1; i < vm.cylinders.all.length; i++) {
        p = vm.cylinders.all[i];
        xMin = Math.min(xMin, p.xVar);
        xMax = Math.max(xMax, p.xVar);
        yMin = Math.min(yMin, p.yVar);
        yMax = Math.max(yMax, p.yVar);
      }

      // apply transformations to the filters
      vm.setXYFilter(xMin, xMax, yMin, yMax);
      vm.squareFilters();
      vm.padFilters();

      // finally set the extents to the current filters
      vm.setXYExtent(
        vm.filter.x[0],
        vm.filter.x[1],
        vm.filter.y[0],
        vm.filter.y[1]
      );
    },

    setXYFilter(xMin, xMax, yMin, yMax) {
      let vm = this;
      // store values
      vm.filter.x[0] = xMin;
      vm.filter.x[1] = xMax;
      vm.filter.y[0] = yMin;
      vm.filter.y[1] = yMax;
      // get raw diffs
      vm.filter.dx = xMax - xMin;
      vm.filter.dy = yMax - yMin;
      // get haversine dist (in cm)
      vm.filter.hav_dist.x.y_min = getHaversineDist(yMin, xMin, yMin, xMax);
      vm.filter.hav_dist.x.y_max = getHaversineDist(yMax, xMin, yMax, xMax);
      vm.filter.hav_dist.y = getHaversineDist(yMin, xMin, yMax, xMin);
    },

    setXYExtent(xMin, xMax, yMin, yMax) {
      let vm = this;
      vm.filter.extent.x[0] = xMin;
      vm.filter.extent.x[1] = xMax;
      vm.filter.extent.y[0] = yMin;
      vm.filter.extent.y[1] = yMax;
    },

    minFilters() {
      let vm = this;
      // if diff is < ~50m, apply a buffer to get extents to be ~50m
      let bufferX = vm.filter.dx < 5e-4 ? (5e-4 - vm.filter.dx) / 2 : 0;
      let bufferY = vm.filter.dy < 5e-4 ? (5e-4 - vm.filter.dy) / 2 : 0;
      if ((bufferX > 0) | (bufferY > 0)) {
        vm.setXYFilter(
          vm.filter.x[0] - bufferX,
          vm.filter.x[1] + bufferX,
          vm.filter.y[0] - bufferY,
          vm.filter.y[1] + bufferY
        );
      }
    },

    squareFilters() {
      let vm = this;
      // make the extents square
      let adjustX =
        vm.filter.dx < vm.filter.dy ? (vm.filter.dy - vm.filter.dx) / 2 : 0;
      let adjustY =
        vm.filter.dy < vm.filter.dx ? (vm.filter.dx - vm.filter.dy) / 2 : 0;
      if ((adjustX > 0) | (adjustY > 0)) {
        vm.setXYFilter(
          vm.filter.x[0] - adjustX,
          vm.filter.x[1] + adjustX,
          vm.filter.y[0] - adjustY,
          vm.filter.y[1] + adjustY
        );
      }
    },

    padFilters() {
      let vm = this;
      // pad the filters by 1/20 of viewport window to give a border around points
      const padX = vm.filter.dx / 20;
      const padY = vm.filter.dy / 20;
      vm.setXYFilter(
        vm.filter.x[0] - padX,
        vm.filter.x[1] + padX,
        vm.filter.y[0] - padY,
        vm.filter.y[1] + padY
      );
    },

    filterBySite() {
      let vm = this;
      let xMin, xMax, yMin, yMax;
      if (vm.site == "All Sites") {
        // set initial filter to first point
        let p = vm.cylinders.all[0];
        xMin = p.xVar;
        xMax = p.xVar;
        yMin = p.yVar;
        yMax = p.yVar;
        for (let i = 1; i < vm.cylinders.all.length; i++) {
          p = vm.cylinders.all[i];
          xMin = Math.min(xMin, p.xVar);
          xMax = Math.max(xMax, p.xVar);
          yMin = Math.min(yMin, p.yVar);
          yMax = Math.max(yMax, p.yVar);
        }
      } else {
        // set initial filter to first point contained in the filter
        let i = 0;
        while (vm.site !== vm.cylinders.all[i]["Location"]) i++;
        let p = vm.cylinders.all[i];
        xMin = p.xVar;
        xMax = p.xVar;
        yMin = p.yVar;
        yMax = p.yVar;
        i++;
        for (i; i < vm.cylinders.all.length; i++) {
          p = vm.cylinders.all[i];
          if (vm.site == p["Location"]) {
            xMin = Math.min(xMin, p.xVar);
            xMax = Math.max(xMax, p.xVar);
            yMin = Math.min(yMin, p.yVar);
            yMax = Math.max(yMax, p.yVar);
          }
        }
      }
      vm.filter.stack = []; // start a new filter stack
      vm.setXYFilter(xMin, xMax, yMin, yMax);
      vm.minFilters();
      vm.squareFilters();
      vm.padFilters();
    },

    undo(operation) {
      let vm = this;
      switch (operation) {
        case "Draw": {
          // remove previously drawn element(s)
          const [id] = vm.dragElement.popElementFromStack();
          if (Number.isSafeInteger(id)) {
            vm.marksGroup.selectAll(`.drag-path-${id}`).remove();
          }
          break;
        }
        case "Zoom":
          // restore the previous filter, if possible
          if (vm.filter.stack.length > 0) {
            vm.filter = vm.filter.stack.pop();
            vm.draw();
          }
          break;
      }
    },

    redoDrawing() {
      // TODO
    },

    deleteDrawing() {
      let vm = this;
      const n = vm.dragElement.elementStack.length;
      // pop from the element stack until no more id's are found
      for (let i = 0; i < n; i++) {
        const [id] = vm.dragElement.popElementFromStack();
        if (Number.isSafeInteger(id)) {
          vm.marksGroup.selectAll(`.drag-path-${id}`).remove();
        }
      }
    },

    resetView() {
      let vm = this;
      vm.filter.stack = []; // reset filter stack
      vm.setXYFilter(
        vm.filter.extent.x[0],
        vm.filter.extent.x[1],
        vm.filter.extent.y[0],
        vm.filter.extent.y[1]
      );
      vm.draw();
    },

    toggleSelectionBorder() {
      let vm = this;
      vm.cylinders.selection.border.show = !vm.cylinders.selection.border.show;
      select(".bound-box").attr("opacity", () =>
        vm.cylinders.selection.border.show ? 1 : 0
      );
    },

    async loadBackgroundData() {
      let vm = this;
      // const tiff = await fetch(vm.background_data.tif).then((response) =>
      //   response.arrayBuffer().then((buffer) => GeoTIFF.fromArrayBuffer(buffer))
      // );
      // const image = await tiff.getImage();
      // vm.background_data.meta = {
      //   width: image.getWidth(),
      //   height: image.getHeight(),
      //   tileWidth: image.getTileWidth(),
      //   tileHeight: image.getTileHeight(),
      //   samplesPerPixel: image.getSamplesPerPixel(),
      //   origin: image.getOrigin(),
      //   resolution: image.getResolution(),
      //   bbox: image.getBoundingBox(),
      // };
      vm.background_data.meta = await fetch(vm.background_data.json).then(
        (response) => response.text().then((contents) => JSON.parse(contents))
      );
      return vm.background_data.meta;
    },

    draw() {
      let vm = this;
      if (!vm.cylinders.all) return; // if there's no dataset don't update the scatter plot

      // update domains to fit the square domains into non-square ranges
      let xScale, yScale;
      let xDomain, yDomain;
      let xRange = [0, vm.plotWidth];
      let yRange = [vm.plotHeight, 0];
      if (vm.plotWidth < vm.plotHeight) {
        xDomain = vm.filter.x;
        // we can use the xScale since the filter bounds are already squared
        // by the squareFilter() function; i.e., the change in degrees in the x
        // axis is the same as the change in degrees in the y axis, or dx = dy
        xScale = scaleLinear().domain(xDomain).range(xRange);
        const diff = vm.plotHeight - vm.plotWidth; // in px
        const adjustY = xScale.invert(diff / 2) - xScale.invert(0); // in degrees
        yDomain = [vm.filter.y[0] - adjustY, vm.filter.y[1] + adjustY];
        yScale = scaleLinear().domain(yDomain).range(yRange);
      } else if (vm.plotWidth > vm.plotHeight) {
        // we can use the yScale since the filter bounds are already squared
        // by the squareFilter() function; i.e., the change in degrees in the x
        // axis is the same as the change in degrees in the y axis, or dx = dy
        yDomain = vm.filter.y;
        yScale = scaleLinear().domain(yDomain).range(yRange);
        const diff = vm.plotWidth - vm.plotHeight; // in px
        const adjustX =
          yScale.invert(vm.plotHeight - diff / 2) -
          yScale.invert(vm.plotHeight); // in degrees
        xDomain = [vm.filter.x[0] - adjustX, vm.filter.x[1] + adjustX];
        xScale = scaleLinear().domain(xDomain).range(xRange);
      } else {
        // already square plot
        xDomain = vm.filter.x;
        xScale = scaleLinear().domain(xDomain).range(xRange);
        yDomain = vm.filter.y;
        yScale = scaleLinear().domain(yDomain).range(yRange);
      }

      // set scales
      vm.xScale = xScale;
      vm.yScale = yScale;

      // set axes
      vm.xAxis = axisTop(vm.xScale);
      vm.yAxis = axisLeft(vm.yScale);

      // draw axes
      vm.xAxisGroup.call(vm.xAxis);
      vm.yAxisGroup.call(vm.yAxis);

      // draw axis titles

      // get haversine x distance formatted with unit
      let xOutput;
      const xDist = vm.filter.hav_dist.x.y_min; // using haversine x at y_min in cm
      if (xDist < 100) {
        xOutput = `${Math.round((xDist + Number.EPSILON) * 100) / 100}cm`;
      } else if (xDist < 100000) {
        xOutput = `${Math.round((xDist / 100 + Number.EPSILON) * 100) / 100}m`;
      } else if (xDist < 100000000) {
        xOutput = `${
          Math.round((xDist / 100000 + Number.EPSILON) * 100) / 100
        }km`;
      } else {
        xOutput = "Unknown";
      }

      // get haversine y distance formatted with unit
      let yOutput;
      const yDist = vm.filter.hav_dist.y; // using haversine y at x_min in cm
      if (yDist < 100) {
        yOutput = `${Math.round((yDist + Number.EPSILON) * 100) / 100}cm`;
      } else if (yDist < 100000) {
        yOutput = `${Math.round((yDist / 100 + Number.EPSILON) * 100) / 100}m`;
      } else if (yDist < 100000000) {
        yOutput = `${
          Math.round((yDist / 100000 + Number.EPSILON) * 100) / 100
        }km`;
      } else {
        yOutput = "Unknown";
      }

      let xAxisTitle = `Longitude | ${xOutput}`;
      let yAxisTitle = `Latitude | ${yOutput}`;

      vm.xAxisGroup.select(".x.axis.title").remove();
      vm.xAxisGroup
        .append("g")
        .classed("x axis title", true)
        .attr("opacity", 1)
        .attr("transform", `translate(${vm.plotWidth / 2}, 0)`)
        .append("text")
        .attr("text-anchor", "middle")
        .attr("fill", "currentColor")
        .attr("y", "-9")
        .attr("dy", "-1.5em")
        .text(xAxisTitle);

      vm.yAxisGroup.select(".y.axis.title").remove();
      vm.yAxisGroup
        .append("g")
        .classed("y axis title", true)
        .attr("opacity", 1)
        .attr("transform", `translate(-25, ${vm.plotHeight / 2})`)
        .append("text")
        .attr("fill", "currentColor")
        .attr("y", "9")
        .text(yAxisTitle);

      // prepare data labels for yAxis
      vm.yAxisGroup
        .selectAll("text")
        .style("text-anchor", "middle")
        .attr("dx", "1.0em")
        .attr("dy", "-1.0em")
        .attr("transform", "rotate(-90)");

      // stagger every other tick label
      vm.xAxisGroup
        .selectAll(".tick line")
        .attr("y2", (_, i) => (i % 2 == 1 ? 0 : -4));
      vm.xAxisGroup
        .selectAll(".tick text")
        .attr("opacity", (_, i) => (i % 2 == 1 ? 0 : 1))
        .attr("dy", (_, i) => (i % 2 == 1 ? "-0.75em" : "0em"));
      vm.yAxisGroup
        .selectAll(".tick line")
        .attr("x2", (_, i) => (i % 2 == 1 ? 0 : -4));
      vm.yAxisGroup
        .selectAll(".tick text")
        .attr("opacity", (_, i) => (i % 2 == 1 ? 0 : 1))
        .attr("dy", (_, i) => (i % 2 == 1 ? "-1.75em" : "-1.0em"));

      // add gridlines
      let xGridlines = axisTop()
        .tickFormat("")
        .tickSize(-vm.plotHeight)
        .scale(vm.xScale);
      vm.xGridlinesGroup.select("*").remove();
      vm.xGridlinesGroup
        .call(xGridlines)
        .call((g) => g.select(".domain").remove());
      let yGridlines = axisRight()
        .tickFormat("")
        .tickSize(vm.plotWidth)
        .scale(vm.yScale);
      vm.yGridlinesGroup.select("*").remove();
      vm.yGridlinesGroup
        .call(yGridlines)
        .call((g) => g.select(".domain").remove());

      // Define the component for the tooltip
      selectAll(".tooltip").remove();
      let tooltip = select("#map-container")
        .append("div")
        .attr("class", "tooltip v-card v-sheet theme--light")
        .style("opacity", 0);
      let tooltipContainer = tooltip
        .append("div")
        .attr("class", "container container--fluid light pa-0");
      let tooltipTitle = tooltipContainer
        .append("div")
        .attr("class", "tooltip-title theme--light ft-lg px-5 pt-5 pb-1");
      let tooltipBody = tooltipContainer
        .append("div")
        .attr("class", "tooltip-body theme--light ft-md px-5 pt-1 pb-5");
      let tooltipFooter = tooltipContainer
        .append("div")
        .attr("class", "tooltip-footer theme--light ft-lg pa-5");

      // filter list of data points
      let prepared = vm.cylinders.all.filter((p) => {
        const dSplit = p["Date"].split("-"); // [yyyy, mm, dd]
        const date = new Date(dSplit[0], dSplit[1], dSplit[2]);
        return (
          p.xVar >= xDomain[0] &&
          p.xVar <= xDomain[1] &&
          p.yVar >= yDomain[0] &&
          p.yVar <= yDomain[1] &&
          date >= vm.startDate &&
          date <= vm.endDate &&
          vm.fates.indexOf(p.Type) !== -1
        );
      });

      // JOIN data selection
      let dataBound = vm.marksGroup.selectAll(".post").data(prepared);

      // DELETE extra points
      dataBound.exit().remove();

      // ENTER new points
      let enterSelection = dataBound.enter().append("g").classed("post", true);

      // UPDATE all existing points
      enterSelection.append("circle");
      enterSelection
        .merge(dataBound)
        .select("circle")
        .attr(
          "transform",
          (d) => `translate(${vm.xScale(d["xVar"])},${vm.yScale(d["yVar"])})`
        )
        .attr("r", 6)
        .style("fill", "white")
        .style("fill-opacity", 0.8)
        .style("stroke-width", (d) => {
          const selected = vm.cylinders.selected.indexOf(d.Cylinder) !== -1;
          return selected ? "3px" : "1px";
        })
        .style("stroke", (d) => {
          const selected = vm.cylinders.selected.indexOf(d.Cylinder) !== -1;
          return selected ? "#2196f3" : "black";
        })
        .style("cursor", "pointer")
        .on("click", function (_, d) {
          if (vm.cylinders.selection.allowed) {
            // toggle selected state of the clicked point
            const index = vm.cylinders.selected.indexOf(d.Cylinder);
            if (index !== -1) {
              select(this)
                .style("stroke", "black")
                .style("stroke-width", "1px");
              vm.cylinders.selected.splice(index, 1);
              vm.$emit("updateSelectedCylinders", vm.cylinders.selected);
            } else {
              select(this)
                .style("stroke", "#2196f3")
                .style("stroke-width", "3px");
              vm.cylinders.selected.push(d.Cylinder);
              vm.$emit("updateSelectedCylinders", vm.cylinders.selected);
            }
            // update tooltip
            tooltipFooter.html(
              `
              <span>Click to ${index === -1 ? "deselect" : "select"}</span>
            `
            );
            // update bounding box, if possible
            vm.drawBoundingBox();
          }
        })
        .on("mouseover", function (e, d) {
          // fade tooltip in
          tooltip
            .style("display", "block")
            .transition()
            .duration(200)
            .style("opacity", 1.0);
          // position tooltip
          let left = e.x + 28;
          let top = e.y - 176;
          if (e.y > window.innerHeight - 240) {
            top -= 240;
          }
          tooltip.style("left", left + "px").style("top", top + "px");
          // add tooltip text
          tooltipTitle.html(d.Cylinder);
          tooltipBody.html(
            `
              <span>Location: ${d.Location}</span>
              <br />
              <span>Type: ${d.Type}</span>
              <br />
              <span>Date: ${d.Date}</span>
              <br />
              <br />
              <span>Lat: ${d.yVar}</span>
              <br />
              <span>Lon: ${d.xVar}</span>
            `
          );
          const selected = vm.cylinders.selected.indexOf(d.Cylinder) !== -1;
          tooltipFooter.html(
            `
              <span>Click to ${selected ? "deselect" : "select"}</span>
            `
          );
        })
        .on("mousemove", function (e) {
          // update tooltip position
          let left = e.x + 28;
          let top = e.y - 176;
          if (e.y > window.innerHeight - 240) {
            top -= 240;
          }
          tooltip.style("left", left + "px").style("top", top + "px");
        })
        .on("mouseout", function () {
          // fade tooltip out and make it non-interactable
          tooltip
            .transition()
            .duration(200)
            .style("opacity", 0)
            .transition()
            .duration(200)
            .style("display", "none");
        });

      // draw bounding box around selected points, if possible
      vm.drawBoundingBox();

      // finally update the background PNG
      if (vm.background && vm.background !== "None") {
        vm.bgGroup
          .select("image")
          .attr("x", vm.xScale(vm.background_data.meta.bbox[0]))
          .attr("y", vm.yScale(vm.background_data.meta.bbox[3]))
          .attr(
            "width",
            vm.xScale(vm.background_data.meta.bbox[2]) -
              vm.xScale(vm.background_data.meta.bbox[0])
          )
          .attr(
            "height",
            vm.yScale(vm.background_data.meta.bbox[1]) -
              vm.yScale(vm.background_data.meta.bbox[3])
          );
      }
    },

    drawBoundingBox() {
      let vm = this;

      // remove bounding box around selected points, if possible
      vm.cylinders.selection.border.exists = false;
      vm.marksGroup.select(".bound-box").remove();

      if (vm.cylinders.selected.length > 1) {
        // get all selected cylinders from all cylinders list
        const selectedSet = new Set(vm.cylinders.selected);
        const points = [...new Set(vm.cylinders.all)].filter((x) =>
          selectedSet.has(x.Cylinder)
        );

        // get bounding box coords around points
        let xMin, xMax, yMin, yMax;
        let p = points[0];
        xMin = p.xVar;
        xMax = p.xVar;
        yMin = p.yVar;
        yMax = p.yVar;
        for (let i = 1; i < points.length; i++) {
          p = points[i];
          xMin = Math.min(xMin, p.xVar);
          xMax = Math.max(xMax, p.xVar);
          yMin = Math.min(yMin, p.yVar);
          yMax = Math.max(yMax, p.yVar);
        }

        // convert coords to px, where (x1, y1) is top-left and (x2, y2) is bottom-right
        let x1 = vm.xScale(xMin);
        let x2 = vm.xScale(xMax);
        let y1 = vm.yScale(yMax);
        let y2 = vm.yScale(yMin);

        // at least one side of the boundary has to be at least 1x point diameter
        // in order to resolve the boundary. that is, the centers of the points
        // inside the boundary have to be at least 1x diameter apart, which
        // would imply they are just touching on either axis

        if (x2 - x1 > 12 || y2 - y1 > 12) {
          // pad the bounds by 1x diameter to make it surround the points nicely
          const pad = 12;
          x1 -= pad;
          x2 += pad;
          y1 -= pad;
          y2 += pad;

          // create the bounding box group
          let bboxGroup = vm.marksGroup
            .select("svg")
            .append("g")
            .classed("bound-box", true)
            .attr("opacity", () =>
              vm.cylinders.selection.border.show ? 1 : 0
            );

          // add border rectangle
          bboxGroup
            .append("rect")
            .attr("x", x1)
            .attr("y", y1)
            .attr("width", x2 - x1)
            .attr("height", y2 - y1)
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("stroke", "#ffffff")
            .attr("stroke-width", "3px")
            .attr("stroke-opacity", 1)
            .attr("fill", "white")
            .attr("fill-opacity", 0.1);

          // add unicorn horn
          const a = Math.max(0.1 * (x2 - x1), 16); // side length => MAX 10% of width or 16px
          const h = (Math.sqrt(3) / 2) * a; // height of equilateral triangle with sides a
          const cx = (x2 + x1) / 2; // x coord => center of border
          bboxGroup
            .append("polygon")
            .attr(
              "points",
              `${cx - a / 2}, ${y1} ${cx + a / 2}, ${y1} ${cx}, ${y1 - h}`
            )
            .attr("stroke", "#ffffff")
            .attr("stroke-width", "1px")
            .attr("stroke-opacity", 1)
            .attr("fill", "white")
            .attr("fill-opacity", 1)
            .attr("stroke-linejoin", "round");

          // add North (N) to the triangle
          bboxGroup
            .append("text")
            .attr("x", cx)
            .attr("y", y1 - h / 3)
            .attr("font-size", a / 2)
            .attr("text-anchor", "middle")
            .attr("dominant-baseline", "central")
            .html("N");

          // set flags to enable controls
          vm.cylinders.selection.border.exists = true;
        }
      }
    },
  },
};
</script>

<style>
#map-container {
  border-radius: 0px;
}

#map-container .v-speed-dial {
  position: absolute;
}

#map-container .v-speed-dial .v-speed-dial__list {
  left: auto;
  right: 0;
  width: auto;
}

#map-container .v-btn--floating {
  position: relative;
}

.list-item-rounded,
.list-item-rounded::before {
  border-radius: 4px !important;
}

.x-gridlines line,
.y-gridlines line {
  stroke: #ccc;
}

.x-gridlines .tick,
.y-gridlines .tick {
  opacity: 0.7;
}

.x.axis .tick text,
.y.axis .tick text {
  font-size: 0.6rem;
}

.x.axis.title text,
.y.axis.title text {
  font-size: 0.7rem;
  font-weight: 800 !important;
}

.bound-box {
  -webkit-filter: drop-shadow(3px 3px 2px rgba(0, 0, 0, 0.7));
  filter: drop-shadow(3px 3px 2px rgba(0, 0, 0, 0.7));
  /* Similar syntax to box-shadow */
}

.tooltip {
  position: absolute !important;
  z-index: 8 !important;
  white-space: nowrap !important;
}

.tooltip-title {
  font-weight: 500;
}

.tooltip-footer {
  color: #ffffff;
  background-color: #2196f3;
}

.tooltip,
.tooltip-footer {
  border-bottom-right-radius: 4px !important;
  border-bottom-left-radius: 4px !important;
}
</style>
