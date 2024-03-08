<template>
  <v-card id="interp-container">
    <v-container fluid class="pa-7">
      <!-- TOP -->
      <v-row id="interp-top-controls-container" class="flex-nowrap pr-3">
        <!-- TOP-LEFT -->
        <v-col cols="11">
          <!-- VALUE SLIDER -->
          <v-range-slider
            v-if="variableHasData"
            dense
            hide-details
            class="value-slider slider-border px-2"
            v-model="variable.filter"
            :style="sliderProps"
            :thumb-color="'#C4C4C4'"
            :min="bounds[variable.name][0]"
            :max="bounds[variable.name][1]"
            :step="variable.step"
            @input="cleanLimited"
          >
            <template v-slot:prepend>
              <v-container fluid class="pa-0">
                <v-row
                  no-gutters
                  class="flex-nowrap"
                  style="height: 24px"
                  align-items="center"
                >
                  <label
                    class="v-label theme--dark pr-2"
                    style="height: 1rem; align-self: center"
                  >
                    Values
                  </label>
                  <label
                    class="v-label theme--dark text-right"
                    style="height: 1rem; align-self: center; width: 72px"
                  >
                    {{
                      Math.round(
                        (variable.filter[0] + Number.EPSILON) *
                          (1 / variable.step)
                      ) /
                      (1 / variable.step)
                    }}
                  </label>
                </v-row>
              </v-container>
            </template>
            <template v-slot:append>
              <v-container fluid class="pa-0">
                <v-row
                  no-gutters
                  class="flex-nowrap"
                  style="height: 24px"
                  align-items="center"
                >
                  <label
                    class="v-label theme--dark text-left"
                    style="height: 1rem; align-self: center; width: 72px"
                  >
                    {{
                      Math.round(
                        (variable.filter[1] + Number.EPSILON) *
                          (1 / variable.step)
                      ) /
                      (1 / variable.step)
                    }}
                  </label>
                </v-row>
              </v-container>
            </template>
          </v-range-slider>

          <!-- NO DATA MESSAGE -->
          <v-container v-else fluid class="pa-0">
            <v-row justify="center">
              <v-card>
                <v-card-title class="pa-0">
                  No data for the selected variable
                </v-card-title>
              </v-card>
            </v-row>
          </v-container>
        </v-col>

        <!-- TOP-RIGHT -->
        <v-col cols="1" class="pa-0 text-center" align-self="center">
          <!-- ORBIT CONTROLS -->
          <v-btn disabled icon>
            <v-icon>{{ icons.mdiCameraControl }}</v-icon>
          </v-btn>
        </v-col>
      </v-row>

      <!-- MIDDLE -->
      <v-row class="pr-3 flex-nowrap">
        <!-- MIDDLE-LEFT -->
        <v-col cols="11" id="canvas-container" class="py-0">
          <!-- CANVAS -->
          <canvas id="cvs"></canvas>
        </v-col>

        <!-- MIDDLE-RIGHT -->
        <v-col
          cols="1"
          id="right-controls-container"
          class="slider-border pa-0"
        >
          <!-- DEPTH SLIDER -->
          <div class="depth-slider-label">
            <label class="v-label theme--dark">Dep</label>
          </div>

          <!-- <v-btn
            icon
            x-small
            style="width: 100%"
            :color="clipPlanes.y.global ? 'primary' : 'default'"
            @click="toggleYClipGlobal"
          >
            <v-icon>{{ icons.mdiEarth }}</v-icon>
          </v-btn> -->

          <!-- <v-btn
            icon
            x-small
            style="width: 100%"
            :color="yClipPlaneHelperVisible ? 'primary' : 'default'"
            @click="toggleYClipHelper"
          >
            <v-icon>{{ icons.mdiGrid }}</v-icon>
          </v-btn> -->

          <v-btn
            icon
            x-small
            style="width: 100%"
            :disabled="!variableHasData"
            :color="
              Math.sign(clipPlanes.y.normal.y) > 0 ? 'primary' : 'default'
            "
            @click="toggleYClipNormal"
          >
            <v-icon>{{ icons.mdiFlipHorizontal }}</v-icon>
          </v-btn>

          <v-slider
            hide-details
            vertical
            class="depth-slider px-3 py-0"
            v-model="clipPlanes.y.value"
            :disabled="!variableHasData"
            :thumb-color="'#C4C4C4'"
            :min="clipPlanes.y.bounds[1]"
            :max="clipPlanes.y.bounds[0]"
            :step="clipPlanes.y.step"
            @input="updateObjects"
          ></v-slider>
        </v-col>
      </v-row>

      <!-- BOTTOM -->
      <v-row id="interp-bottom-controls-container" class="flex-nowrap pr-3">
        <!-- BOTTOM-LEFT -->
        <v-col cols="11">
          <v-row>
            <!-- LAT SLIDER -->
            <v-col cols="6" class="pr-1">
              <v-slider
                dense
                hide-details
                class="slider-border px-2"
                v-model="clipPlanes.z.value"
                :disabled="!variableHasData"
                :thumb-color="'#C4C4C4'"
                :min="clipPlanes.z.bounds[0]"
                :max="clipPlanes.z.bounds[1]"
                :step="clipPlanes.z.step"
                @input="updateObjects"
              >
                <template v-slot:prepend>
                  <v-container fluid class="pa-0">
                    <v-row no-gutters class="flex-nowrap">
                      <label
                        class="v-label theme--dark pr-2"
                        style="height: 1rem; align-self: center"
                      >
                        Lat
                      </label>

                      <!-- <v-btn
                        icon
                        x-small
                        class="mx-1"
                        :color="clipPlanes.z.global ? 'primary' : 'default'"
                        @click="toggleZClipGlobal"
                      >
                        <v-icon>{{ icons.mdiEarth }}</v-icon>
                      </v-btn> -->

                      <!-- <v-btn
                        icon
                        x-small
                        class="mx-1"
                        :color="zClipPlaneHelperVisible ? 'primary' : 'default'"
                        @click="toggleZClipHelper"
                      >
                        <v-icon>{{ icons.mdiGrid }}</v-icon>
                      </v-btn> -->

                      <v-btn
                        icon
                        x-small
                        class="mx-1"
                        :disabled="!variableHasData"
                        :color="
                          Math.sign(clipPlanes.z.normal.z) > 0
                            ? 'primary'
                            : 'default'
                        "
                        @click="toggleZClipNormal"
                      >
                        <v-icon>{{ icons.mdiFlipHorizontal }}</v-icon>
                      </v-btn>
                    </v-row>
                  </v-container>
                </template>
              </v-slider>
            </v-col>

            <!-- LON SLIDER -->
            <v-col cols="6" class="pl-1">
              <v-slider
                dense
                hide-details
                class="slider-border px-2"
                v-model="clipPlanes.x.value"
                :disabled="!variableHasData"
                :thumb-color="'#C4C4C4'"
                :min="clipPlanes.x.bounds[0]"
                :max="clipPlanes.x.bounds[1]"
                :step="clipPlanes.x.step"
                @input="updateObjects"
              >
                <template v-slot:prepend>
                  <v-container fluid class="pa-0">
                    <v-row no-gutters class="flex-nowrap">
                      <label
                        class="v-label theme--dark pr-2"
                        style="height: 1rem; align-self: center"
                      >
                        Lon
                      </label>

                      <!-- <v-btn
                        icon
                        x-small
                        class="mx-1"
                        :color="clipPlanes.x.global ? 'primary' : 'default'"
                        @click="toggleXClipGlobal"
                      >
                        <v-icon>{{ icons.mdiEarth }}</v-icon>
                      </v-btn> -->

                      <!-- <v-btn
                        icon
                        x-small
                        class="mx-1"
                        :color="xClipPlaneHelperVisible ? 'primary' : 'default'"
                        @click="toggleXClipHelper"
                      >
                        <v-icon>{{ icons.mdiGrid }}</v-icon>
                      </v-btn> -->

                      <v-btn
                        icon
                        x-small
                        class="mx-1"
                        :disabled="!variableHasData"
                        :color="
                          -Math.sign(clipPlanes.x.normal.x) > 0
                            ? 'primary'
                            : 'default'
                        "
                        @click="toggleXClipNormal"
                      >
                        <v-icon>{{ icons.mdiFlipHorizontal }}</v-icon>
                      </v-btn>
                    </v-row>
                  </v-container>
                </template>
              </v-slider>
            </v-col>
          </v-row>
        </v-col>

        <!-- BOTTOM-RIGHT -->
        <v-col cols="1" class="pa-0 text-center" align-self="center">
          <!-- DOWNLOAD INTERPOLATION -->
          <v-btn disabled icon>
            <v-icon>{{ icons.mdiDownload }}</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import {
  mdiCameraControl,
  mdiEarth,
  mdiGrid,
  mdiFlipHorizontal,
  mdiDownload,
} from "@mdi/js";
import throttle from "lodash/throttle";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import * as vsup from "vsup";

import craneGeometryJSON from "@/models/3D/craneGeometry.json";

function countDecimals(value) {
  if (Math.floor(value) === value) return 0;
  let result;
  let str = value.toString();
  if (str.indexOf(".") !== -1 && str.indexOf("-") !== -1) {
    result = str.split("-")[1] || 0;
  } else if (str.indexOf(".") !== -1) {
    result = str.split(".")[1].length || 0;
  } else {
    result = str.split("-")[1] || 0;
  }
  return result;
}

class clipPlane {
  constructor(normal, constant) {
    this.plane = new THREE.Plane(normal, constant);
    this.value = 0;
    this.step = 1;
    this.bounds = [0, 0];
    this.global = false;
    this.helper = undefined;
  }
}

Object.defineProperty(clipPlane.prototype, "normal", {
  get() {
    return this.plane.normal;
  },
  set(val) {
    this.plane.set(val, this.plane.constant);
  },
});

Object.defineProperty(clipPlane.prototype, "constant", {
  get() {
    return this.plane.constant;
  },
  set(val) {
    this.plane.set(this.plane.normal, val);
  },
});

export default {
  name: "InterpView",

  props: {
    interpData: {
      type: Array,
      default: () => [],
    },
    cylinders: {
      type: Array,
      default: () => [],
    },
    variables: {
      type: Array,
      default: () => [],
    },
    variablesChanged: {
      type: Boolean,
      default: () => false,
    },
    resolution: {
      type: Number,
      default: () => 0,
    },
    resolutionChanged: {
      type: Boolean,
      default: () => false,
    },
    colorMode: {
      type: String,
      default: () => "",
    },
    cmap: {
      type: Function,
      default: () => function () {},
    },
    shapeType: {
      type: String,
      default: () => "",
    },
    showValues: {
      type: Boolean,
      default: () => false,
    },
    geoHeight: {
      type: Number,
      default: () => 0,
    },
    mouseMode: {
      type: String,
      default: () => "",
    },
  },

  data: () => ({
    icons: {
      mdiCameraControl: mdiCameraControl,
      mdiEarth: mdiEarth,
      mdiGrid: mdiGrid,
      mdiFlipHorizontal: mdiFlipHorizontal,
      mdiDownload: mdiDownload,
    },

    // threejs variables and helpers
    canvas: undefined,
    renderer: undefined,
    camera: undefined,
    scene: undefined,
    controls: undefined,
    light1: undefined,
    light2: undefined,
    raycaster: undefined,
    mouse: undefined,
    gridHelper: undefined,
    axesHelper: undefined,
    frustumHelper: undefined,
    objects: [],
    craneGeometry: undefined,
    matrix: new THREE.Matrix4(), // dummy matrix helper
    color: new THREE.Color(), // dummy color helper
    clipPlanes: {
      x: new clipPlane(new THREE.Vector3(1, 0, 0), 0),
      y: new clipPlane(new THREE.Vector3(0, -1, 0), 0),
      z: new clipPlane(new THREE.Vector3(0, 0, -1), 0),
    },

    // input parameters
    bounds: {},
    variable: {
      name: null,
      filter: [null, null],
      step: null,
    },

    // flags
    orbitControlsActive: true, // flag for whether to allow orbit controls
    renderRequested: false, // flag for whether to re-render or not
    gridHelperVisible: false, // hide grid helper by default
    axesHelperVisible: false, // show axes helper by default
    frustumHelperVisible: false, // hide frustum helper by default
    xClipPlaneHelperVisible: false, // hide clip plane helpers by default
    yClipPlaneHelperVisible: false,
    zClipPlaneHelperVisible: false,
  }),

  computed: {
    sliderProps() {
      return {
        "--bg-gradient": `linear-gradient(
          90deg, 
          ${this.cmap(0.0)}, 
          ${this.cmap(0.1)},
          ${this.cmap(0.2)},
          ${this.cmap(0.3)},
          ${this.cmap(0.4)},
          ${this.cmap(0.5)},
          ${this.cmap(0.6)}, 
          ${this.cmap(0.7)},
          ${this.cmap(0.8)},
          ${this.cmap(0.9)},
          ${this.cmap(1.0)}
        )`,
      };
    },

    variableHasData() {
      return (
        this.variable.filter[0] !== null &&
        this.variable.filter[1] !== null &&
        this.variable.step !== null
      );
    },
  },

  mounted: function () {
    let vm = this;

    // load crane geometry from file
    const loader = new THREE.BufferGeometryLoader();
    vm.craneGeometry = loader.parse(craneGeometryJSON);
    vm.craneGeometry.translate(-3.255, -2.82, 8); // center on origin

    window.addEventListener("resize", vm.requestRenderIfNotRequested, false);

    // start the show!
    vm.init();
    if (vm.interpData.length > 0) {
      vm.parseData(vm.interpData);
      vm.addObjects();
      vm.requestRenderIfNotRequested();
    }
  },

  watch: {
    interpData: function (newData) {
      let vm = this;
      if (vm.interpData.length > 0) {
        vm.parseData(newData);
        vm.clean();
      }
    },

    cmap: function () {
      this.clean();
    },

    shapeType: function () {
      this.clean();
    },

    geoHeight: function (newGeoHeight) {
      let vm = this;
      // when height changes, need to re-compute the y clip plane constant
      const ySign = Math.sign(vm.clipPlanes.y.normal.y);
      const yInput = -vm.clipPlanes.y.value;
      if (yInput == -vm.clipPlanes.y.bounds[0]) {
        vm.clipPlanes.y.constant = ySign * (yInput * newGeoHeight - 0.01);
      } else if (yInput == -vm.clipPlanes.y.bounds[1]) {
        vm.clipPlanes.y.constant = ySign * (yInput * newGeoHeight + 0.01);
      } else {
        vm.clipPlanes.y.constant = ySign * yInput * newGeoHeight + 0.01;
      }
      // then re-draw
      vm.clean();
    },

    showValues: function () {
      this.clean();
    },

    mouseMode: function (newMouseMode) {
      let vm = this;
      // disable orbit controls if not in "Orbit" mode
      if (newMouseMode == "Orbit") {
        vm.controls.enabled = true;
      } else {
        vm.controls.enabled = false;
      }
      // re-draw the scene
      vm.clean();
    },
  },

  methods: {
    init() {
      let vm = this;
      vm.canvas = document.getElementById("cvs"); // canvas
      vm.canvas.addEventListener("mousemove", vm.onMouseMove, false); // track mouse
      vm.canvas.addEventListener("click", vm.onClick, false); // handle click

      // renderer
      vm.renderer = new THREE.WebGLRenderer({ canvas: vm.canvas });
      vm.renderer.localClippingEnabled = true;

      // scene
      vm.scene = new THREE.Scene();
      vm.scene.background = new THREE.Color(0x121212);

      // camera
      const fov = 50; // field of view
      const aspect = 1; // aspect ratio; the canvas default is 2
      const near = 0.1; // near clipping plane
      const far = 2000; // far clipping plane
      vm.camera = new THREE.PerspectiveCamera(fov, aspect, near, far);

      // controls
      vm.controls = new OrbitControls(vm.camera, vm.canvas);
      vm.controls.listenToKeyEvents(window);
      vm.controls.object.position.set(-100, 100, 100);
      vm.controls.target = new THREE.Vector3(80, 0, -70);
      vm.controls.enableDamping = true;
      vm.controls.dampingFactor = 0.05;
      vm.controls.screenSpacePanning = false;
      vm.controls.minDistance = 0;
      vm.controls.maxDistance = 500;
      vm.controls.maxPolarAngle = Math.PI / 2;
      // vm.controls.mouseButtons = {
      //   LEFT: THREE.MOUSE.PAN,
      //   MIDDLE: THREE.MOUSE.DOLLY,
      //   RIGHT: THREE.MOUSE.ROTATE,
      // };
      vm.controls.addEventListener(
        "change",
        vm.requestRenderIfNotRequested,
        false
      );
      vm.controls.enabled = vm.orbitControlsActive;

      // lights
      vm.light1 = new THREE.HemisphereLight(0xffffff, 0x222222);
      vm.light1.position.set(-1, 1.5, 1);
      vm.scene.add(vm.light1);
      vm.light2 = new THREE.HemisphereLight(0xffffff, 0x222222, 0.5);
      vm.light2.position.set(-1, -1.5, -1);
      vm.scene.add(vm.light2);

      // raycast
      vm.raycaster = new THREE.Raycaster();
      vm.mouse = new THREE.Vector2(1, 1);

      // frustum helper
      // vm.frustumHelper = new THREE.CameraHelper(vm.camera);
      // vm.frustumHelper.name = "frustumHelper";
      // vm.frustumHelper.visible = vm.frustumHelperVisible;
      // vm.scene.add(vm.frustumHelper);

      // grid helper
      // vm.gridHelper = new THREE.GridHelper(1000, 1000, "black", "#C2B280");
      // vm.gridHelper.name = "gridHelper";
      // vm.gridHelper.visible = vm.gridHelperVisible;
      // vm.scene.add(vm.gridHelper);

      // axis helper
      // vm.axesHelper = new THREE.AxesHelper(30);
      // vm.axesHelper.name = "axesHelper";
      // vm.axesHelper.visible = vm.axesHelperVisible;
      // vm.scene.add(vm.axesHelper);

      // plane helpers
      // vm.clipPlanes.x.helper = new THREE.PlaneHelper(
      //   vm.clipPlanes.x.plane,
      //   15,
      //   0xff0000
      // );
      // vm.clipPlanes.x.helper.name = "xClipPlaneHelper";
      // vm.clipPlanes.x.helper.visible = vm.xClipPlaneHelperVisible;
      // vm.clipPlanes.y.helper = new THREE.PlaneHelper(
      //   vm.clipPlanes.y.plane,
      //   15,
      //   0x00ff00
      // );
      // vm.clipPlanes.y.helper.name = "yClipPlaneHelper";
      // vm.clipPlanes.y.helper.visible = vm.yClipPlaneHelperVisible;
      // vm.clipPlanes.z.helper = new THREE.PlaneHelper(
      //   vm.clipPlanes.z.plane,
      //   15,
      //   0x0000ff
      // );
      // vm.clipPlanes.z.helper.name = "zClipPlaneHelper";
      // vm.clipPlanes.z.helper.visible = vm.zClipPlaneHelperVisible;
      // vm.scene.add(vm.clipPlanes.x.helper);
      // vm.scene.add(vm.clipPlanes.y.helper);
      // vm.scene.add(vm.clipPlanes.z.helper);
    },

    parseData(newData) {
      let vm = this;

      vm.variable.name = vm.variables[0]; // set variable

      // create new boundaries data object
      vm.bounds = Object.assign(
        {
          x: [null, null],
          y: [null, null],
          z: [null, null],
          u: [null, null],
        },
        Object.fromEntries(vm.variables.map((x) => [x, [null, null]]))
      );

      // set initial x,y,z,dist bounds using first point
      // these columns are always fully populated, so taking the first
      // value should be fine
      let i = 0;
      let d = newData[i];
      vm.bounds.x[0] = parseFloat(d.X);
      vm.bounds.x[1] = parseFloat(d.X);
      vm.bounds.y[0] = parseFloat(d.Y);
      vm.bounds.y[1] = parseFloat(d.Y);
      vm.bounds.z[0] = parseFloat(d.Z);
      vm.bounds.z[1] = parseFloat(d.Z);
      vm.bounds.u[0] = parseFloat(d["dist_to_nearest"]);
      vm.bounds.u[1] = parseFloat(d["dist_to_nearest"]);

      // some datasets (like linear) have missing values for variables
      // walk through until you can set initial bounds on each variable
      let varSet = vm.variables.map(() => false);
      let stopIter = true;
      for (let j = 0; j < newData.length; j++) {
        for (let k = 0; k < vm.variables.length; k++) {
          if (!varSet[k]) {
            const v = parseFloat(newData[j][vm.variables[k]]);
            if (!Number.isNaN(v)) {
              vm.bounds[vm.variables[k]][0] = v;
              vm.bounds[vm.variables[k]][1] = v;
              varSet[k] = true;
            } else {
              stopIter = false;
            }
          }
        }
        if (stopIter) break;
      }

      // walk through the rest of the points
      for (i = 1; i < newData.length; i++) {
        d = newData[i];
        vm.bounds.x[0] = Math.min(vm.bounds.x[0], parseFloat(d.X));
        vm.bounds.x[1] = Math.max(vm.bounds.x[1], parseFloat(d.X));
        vm.bounds.y[0] = Math.min(vm.bounds.y[0], parseFloat(d.Y));
        vm.bounds.y[1] = Math.max(vm.bounds.y[1], parseFloat(d.Y));
        vm.bounds.z[0] = Math.min(vm.bounds.z[0], parseFloat(d.Z));
        vm.bounds.z[1] = Math.max(vm.bounds.z[1], parseFloat(d.Z));
        vm.bounds.u[0] = Math.min(
          vm.bounds.u[0],
          parseFloat(d["dist_to_nearest"])
        );
        vm.bounds.u[1] = Math.max(
          vm.bounds.u[1],
          parseFloat(d["dist_to_nearest"])
        );
        for (let k = 0; k < vm.variables.length; k++) {
          const v = parseFloat(d[vm.variables[k]]); // returns either "Number" or "NaN"
          if (!Number.isNaN(v)) {
            vm.bounds[vm.variables[k]][0] = Math.min(
              vm.bounds[vm.variables[k]][0],
              v
            );
            vm.bounds[vm.variables[k]][1] = Math.max(
              vm.bounds[vm.variables[k]][1],
              v
            );
          }
        }
      }

      if (vm.variablesChanged) {
        // set value filter to variables bounds
        const lb = vm.bounds[vm.variable.name][0];
        const rb = vm.bounds[vm.variable.name][1];
        vm.variable.filter = [lb, rb];
        if (lb !== null && rb !== null) {
          vm.variable.step = Math.max(
            10 ** -4,
            10 ** -Math.max(countDecimals(lb), countDecimals(rb))
          ); // step is based on decimals or 1e-4, the smallest step size allowed
          vm.$emit("updateInterpVarHasData", true); // tell parent to enable controls
        } else {
          vm.variable.step = null; // bounds are null => no data for the var
          vm.$emit("updateInterpVarHasData", false); // tell parent to disable controls
        }
      }

      if (vm.resolutionChanged) {
        // set clipping plane bounds
        vm.clipPlanes.x.bounds = [
          vm.bounds.x[0],
          vm.bounds.x[1] + vm.resolution,
        ];
        vm.clipPlanes.y.bounds = [-vm.bounds.z[0], -(vm.bounds.z[1] + 1)];
        vm.clipPlanes.z.bounds = [
          vm.bounds.y[0],
          vm.bounds.y[1] + vm.resolution,
        ];
        // set constants, applying small correction to start
        vm.clipPlanes.x.constant =
          -Math.sign(vm.clipPlanes.x.normal.x) * vm.clipPlanes.x.bounds[0] +
          0.01;
        vm.clipPlanes.y.constant =
          Math.sign(vm.clipPlanes.y.normal.y) * -vm.clipPlanes.y.bounds[0] +
          0.01;
        vm.clipPlanes.z.constant =
          Math.sign(vm.clipPlanes.z.normal.z) * vm.clipPlanes.z.bounds[0] +
          0.01;
        // set clipping plane value and step
        vm.clipPlanes.x.value = vm.clipPlanes.x.bounds[0];
        vm.clipPlanes.x.step = vm.resolution;
        vm.clipPlanes.y.value = vm.clipPlanes.y.bounds[0];
        vm.clipPlanes.y.step = 1;
        vm.clipPlanes.z.value = vm.clipPlanes.z.bounds[0];
        vm.clipPlanes.z.step = vm.resolution;
      }

      vm.$emit("resetInterpViewChangedFlags"); // tell the parent to reset the changed flags
    },

    addObjects() {
      let vm = this;

      let instancedMesh;
      let tubeMesh;
      let hornMesh;
      // let coneMesh;
      let craneMesh;
      let hoverLines;

      // only attempt to generate the mesh if there is an active filter set,
      // since the filter is null if the variable to be plotted has equal bounds

      if (vm.variable.filter[0] !== null && vm.variable.filter[1] !== null) {
        // build the geometry
        let geometry;
        switch (vm.shapeType) {
          case "Cylinder": {
            const radiusTop = 7 / 2; // 7cm diameter, top radius
            const radiusBottom = 7 / 2; // 7cm diameter, bottom radius
            const radialEdges = 12;
            geometry = new THREE.CylinderGeometry(
              radiusTop,
              radiusBottom,
              vm.geoHeight,
              radialEdges
            );
            break;
          }
          case "Prism": {
            const width = vm.resolution; // x axis, in cm
            const depth = vm.resolution; // z axis, in cm
            geometry = new THREE.BoxGeometry(width, vm.geoHeight, depth);
            break;
          }
        }
        // build the material
        const material = new THREE.MeshPhongMaterial({
          side: THREE.DoubleSide,
          clippingPlanes: [
            vm.clipPlanes.x.plane,
            vm.clipPlanes.y.plane,
            vm.clipPlanes.z.plane,
          ],
          clipIntersection: true,
        });
        // create a new instanced mesh
        instancedMesh = new THREE.InstancedMesh(
          geometry,
          material,
          vm.interpData.length
        );
        // get color function
        const vBounds = vm.bounds[vm.variable.name]; // get variable bounds
        switch (vm.colorMode) {
          case "Standard": {
            // use standard D3 cmap implementation
            var norm = (v) => (v - vBounds[0]) / (vBounds[1] - vBounds[0]); // normalize values [0, 1]
            vm.$emit("updateColorModeLegend", { legend: null, height: 0 });
            break;
          }
          case "Uncertainty": {
            // create Value-Suppressing Color Palette (VSUP)
            var scale = vsup
              .scale()
              .quantize(
                vsup
                  .quantization()
                  .branching(2)
                  .layers(4)
                  .valueDomain(vBounds)
                  .uncertaintyDomain(vm.bounds.u)
              )
              .range(vm.cmap);
            var arcLegend = vsup.legend
              .arcmapLegend()
              .scale(scale)
              .size(125)
              .x(50)
              .y(50);
            vm.$emit("updateColorModeLegend", {
              legend: arcLegend,
              height: 200,
            });
            break;
          }
        }
        // apply transformations at every vertex to get final shape
        for (let i = 0; i < vm.interpData.length; i++) {
          const dataPoint = vm.interpData[i];
          const o = parseFloat(dataPoint["observed"]);
          if (vm.showValues) {
            const v = parseFloat(dataPoint[vm.variable.name]);
            if (
              !Number.isNaN(v) &&
              v >= vm.variable.filter[0] &&
              v <= vm.variable.filter[1]
            ) {
              // transform
              const x = parseFloat(dataPoint.X);
              const y = parseFloat(dataPoint.Y);
              const z = parseFloat(dataPoint.Z);
              vm.matrix.setPosition(
                x + vm.resolution / 2,
                -vm.geoHeight * (z + 0.5),
                -(y + vm.resolution / 2)
              );
              instancedMesh.setMatrixAt(i, vm.matrix);
              // color
              if (vm.colorMode == "Standard") {
                instancedMesh.setColorAt(i, vm.color.set(vm.cmap(norm(v))));
              } else if (vm.colorMode == "Uncertainty") {
                const u = parseFloat(dataPoint["dist_to_nearest"]);
                instancedMesh.setColorAt(i, vm.color.set(scale(v, u)));
              }
              // outline
              if (o) {
                const edges = new THREE.EdgesGeometry(geometry);
                const line = new THREE.LineSegments(
                  edges,
                  new THREE.LineBasicMaterial({ color: 0xffffff })
                );
                line.geometry.applyMatrix4(vm.matrix);
                vm.scene.add(line);
              }
            }
          } else if (!vm.showValues && o) {
            const v = parseFloat(dataPoint[vm.variable.name]);
            if (
              !Number.isNaN(v) &&
              v >= vm.variable.filter[0] &&
              v <= vm.variable.filter[1]
            ) {
              // transform
              const x = parseFloat(dataPoint.X);
              const y = parseFloat(dataPoint.Y);
              const z = parseFloat(dataPoint.Z);
              vm.matrix.setPosition(
                x + vm.resolution / 2,
                -vm.geoHeight * (z + 0.5),
                -(y + vm.resolution / 2)
              );
              instancedMesh.setMatrixAt(i, vm.matrix);
              // color
              if (vm.colorMode == "Standard") {
                instancedMesh.setColorAt(i, vm.color.set(vm.cmap(norm(v))));
              } else if (vm.colorMode == "Uncertainty") {
                const u = parseFloat(dataPoint["dist_to_nearest"]);
                instancedMesh.setColorAt(i, vm.color.set(scale(v, u)));
              }
              // outline
              // const edges = new THREE.EdgesGeometry(geometry);
              // const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0xffffff }));
              // line.geometry.applyMatrix4(vm.matrix);
              // vm.scene.add(line);
            }
          }
        }
        // add mesh to the scene
        vm.scene.add(instancedMesh);
      }

      // add directional bounding box helper to the scene
      const bboxWidth = vm.clipPlanes.x.bounds[1]; // x-axis
      const bboxHeight = 10; // y-axis
      const bboxDepth = vm.clipPlanes.z.bounds[1]; // z-axis
      const splines = {
        top: new THREE.CatmullRomCurve3([
          new THREE.Vector3(-10, bboxHeight, -(bboxDepth + 10)),
          new THREE.Vector3(bboxWidth + 10, bboxHeight, -(bboxDepth + 10)),
        ]),
        right: new THREE.CatmullRomCurve3([
          new THREE.Vector3(bboxWidth + 10, bboxHeight, -(bboxDepth + 10)),
          new THREE.Vector3(bboxWidth + 10, bboxHeight, 10),
        ]),
        bottom: new THREE.CatmullRomCurve3([
          new THREE.Vector3(bboxWidth + 10, bboxHeight, 10),
          new THREE.Vector3(-10, bboxHeight, 10),
        ]),
        left: new THREE.CatmullRomCurve3([
          new THREE.Vector3(-10, bboxHeight, 10),
          new THREE.Vector3(-10, bboxHeight, -(bboxDepth + 10)),
        ]),
      };
      Object.keys(splines).forEach((key) => {
        const params = {
          path: splines[key],
          tubularSegments: 100,
          radius: 1,
          radialSegments: 20,
          closed: true,
        };
        const tubeGeometry = new THREE.TubeGeometry(
          params.path,
          params.tubularSegments,
          params.radius,
          params.radialSegments,
          params.closed
        );
        const tubeMaterial = new THREE.MeshPhongMaterial({ color: 0xbbbbbb });
        tubeMesh = new THREE.Mesh(tubeGeometry, tubeMaterial);
        vm.scene.add(tubeMesh);
      });

      // create unicorn horn on the directional bounding box helper
      const a = Math.max(0.1 * bboxWidth, 16); // side length => MAX 10% of width or 16 units
      const h = (Math.sqrt(3) / 2) * a; // height of equilateral triangle with sides a
      const hornShape = new THREE.Shape()
        .moveTo(-a / 2, -h / 2)
        .lineTo(a / 2, -h / 2)
        .lineTo(0, h / 2)
        .lineTo(-a / 2, -h / 2); // close path
      const extrudeSettings = {
        steps: 10,
        depth: 1,
        bevelEnabled: false,
      };
      const hornGeometry = new THREE.ExtrudeGeometry(
        hornShape,
        extrudeSettings
      );
      const hornMaterial = new THREE.MeshPhongMaterial({ color: 0xbbbbbb });
      hornMesh = new THREE.Mesh(hornGeometry, hornMaterial);
      hornMesh.rotation.set(-Math.PI / 2, 0, 0);
      hornMesh.position.set(
        vm.clipPlanes.x.bounds[1] / 2,
        bboxHeight,
        -(vm.clipPlanes.z.bounds[1] + h / 2 + 10)
      );
      vm.scene.add(hornMesh);

      // add selected core hover cone
      // let coneRadius;
      // switch (vm.shapeType) {
      //   case "Cylinder": {
      //     coneRadius = 7 / 4; // 7cm diameter
      //     break;
      //   }
      //   case "Prism": {
      //     coneRadius = vm.resolution / 2; // x axis, in cm
      //     break;
      //   }
      // }
      // const coneGeometry = new THREE.ConeGeometry(coneRadius, coneRadius, 3);
      // const coneMaterial = new THREE.MeshPhongMaterial({ color: 0xbbbbbb });
      // coneMesh = new THREE.Mesh(coneGeometry, coneMaterial);
      // coneMesh.rotation.set(-Math.PI, 0, 0);
      // coneMesh.visible = false; // hide in the beginning
      // vm.scene.add(coneMesh);

      // add selected core hover crane
      const craneMaterial = new THREE.MeshPhongMaterial({ color: 0xbbbbbb });
      craneMesh = new THREE.Mesh(vm.craneGeometry, craneMaterial);
      craneMesh.position.set(0, 3, 0); // floating just above the origin
      craneMesh.scale.set(
        vm.resolution * 2,
        vm.resolution * 2,
        vm.resolution * 2
      ); // re-size
      craneMesh.visible = false; // hide in the beginning
      vm.scene.add(craneMesh);

      // add hovered outline to column of data under the cone
      const hoverGeometry = new THREE.BoxGeometry(
        vm.resolution,
        -vm.geoHeight * (vm.bounds.z[1] + 1),
        vm.resolution
      );
      const hoverEdges = new THREE.EdgesGeometry(hoverGeometry);
      hoverLines = new THREE.LineSegments(
        hoverEdges,
        new THREE.LineBasicMaterial({ color: 0x2196f3 })
      );
      hoverLines.visible = false; // hide initially
      vm.scene.add(hoverLines);

      // add crane

      // finally, add all important objects to a list
      vm.objects = [instancedMesh, craneMesh, hoverLines];
    },

    getLinearGradient() {
      return `
        linear-gradient(
          90deg, 
          ${this.cmap(0.0)}, 
          ${this.cmap(0.1)},
          ${this.cmap(0.2)},
          ${this.cmap(0.3)},
          ${this.cmap(0.4)},
          ${this.cmap(0.5)},
          ${this.cmap(0.6)}, 
          ${this.cmap(0.7)},
          ${this.cmap(0.8)},
          ${this.cmap(0.9)},
          ${this.cmap(1.0)}
        )
      `;
    },

    toggleXClipGlobal() {
      this.clipPlanes.x.global = !this.clipPlanes.x.global;
      this.updateObjects();
    },

    toggleXClipHelper() {
      this.xClipPlaneHelperVisible = !this.xClipPlaneHelperVisible;
      this.clipPlanes.x.helper.visible = this.xClipPlaneHelperVisible; // set state
      this.updateObjects();
    },

    toggleXClipNormal() {
      this.clipPlanes.x.normal = this.clipPlanes.x.normal.negate();
      this.updateObjects();
    },

    toggleYClipGlobal() {
      this.clipPlanes.y.global = !this.clipPlanes.y.global;
      this.updateObjects();
    },

    toggleYClipHelper() {
      this.yClipPlaneHelperVisible = !this.yClipPlaneHelperVisible;
      this.clipPlanes.y.helper.visible = this.yClipPlaneHelperVisible; // set state
      this.updateObjects();
    },

    toggleYClipNormal() {
      this.clipPlanes.y.normal = this.clipPlanes.y.normal.negate();
      this.updateObjects();
    },

    toggleZClipGlobal() {
      this.clipPlanes.z.global = !this.clipPlanes.z.global;
      this.updateObjects();
    },

    toggleZClipHelper() {
      this.zClipPlaneHelperVisible = !this.zClipPlaneHelperVisible;
      this.clipPlanes.z.helper.visible = this.zClipPlaneHelperVisible; // set state
      this.updateObjects();
    },

    toggleZClipNormal() {
      this.clipPlanes.z.normal = this.clipPlanes.z.normal.negate();
      this.updateObjects();
    },

    updateObjects() {
      let vm = this;

      // adjust clip planes, correcting at the boundaries to avoid glitchy textures
      // this took forever to figure out... I hope someone appreciates this...

      // x axis
      const xSign = Math.sign(vm.clipPlanes.x.normal.x);
      const xInput = vm.clipPlanes.x.value;
      if (xInput == vm.clipPlanes.x.bounds[0]) {
        vm.clipPlanes.x.constant = -xSign * (xInput - 0.01);
      } else if (xInput == vm.clipPlanes.x.bounds[1]) {
        vm.clipPlanes.x.constant = -xSign * (xInput + 0.01);
      } else {
        vm.clipPlanes.x.constant = -xSign * xInput + 0.01;
      }

      // y axis
      const ySign = Math.sign(vm.clipPlanes.y.normal.y);
      const yInput = -vm.clipPlanes.y.value;
      if (yInput == -vm.clipPlanes.y.bounds[0]) {
        vm.clipPlanes.y.constant = ySign * (yInput * vm.geoHeight - 0.01);
      } else if (yInput == -vm.clipPlanes.y.bounds[1]) {
        vm.clipPlanes.y.constant = ySign * (yInput * vm.geoHeight + 0.01);
      } else {
        vm.clipPlanes.y.constant = ySign * yInput * vm.geoHeight + 0.01;
      }

      // z axis
      const zSign = Math.sign(vm.clipPlanes.z.normal.z);
      const zInput = vm.clipPlanes.z.value;
      if (zInput == vm.clipPlanes.z.bounds[0]) {
        vm.clipPlanes.z.constant = zSign * (zInput - 0.01);
      } else if (zInput == vm.clipPlanes.z.bounds[1]) {
        vm.clipPlanes.z.constant = zSign * (zInput + 0.01);
      } else {
        vm.clipPlanes.z.constant = zSign * zInput + 0.01;
      }

      // set global clip planes, if any are toggled
      // let globalPlanes = [];
      // if (vm.clipPlanes.x.global) globalPlanes.push(vm.clipPlanes.x.plane);
      // if (vm.clipPlanes.y.global) globalPlanes.push(vm.clipPlanes.y.plane);
      // if (vm.clipPlanes.z.global) globalPlanes.push(vm.clipPlanes.z.plane);
      // vm.renderer.clippingPlanes =
      //   globalPlanes.length > 0 ? globalPlanes : Object.freeze([]);

      // re-render
      vm.requestRenderIfNotRequested();
    },

    resetView() {
      let vm = this;

      // update orbit controls camera
      vm.controls.object.position.set(-100, 200, 100);
      vm.controls.target = new THREE.Vector3(80, 30, -70);
      vm.camera.updateProjectionMatrix();

      // reset variable filter, if possible
      const lb = vm.bounds[vm.variable.name][0];
      const rb = vm.bounds[vm.variable.name][1];
      vm.variable.filter = [lb, rb];
      if (lb !== null && rb !== null) {
        vm.variable.step = Math.max(
          10 ** -4,
          10 ** -Math.max(countDecimals(lb), countDecimals(rb))
        ); // step is based on decimals or 1e-4, the smallest step size allowed
        vm.$emit("updateInterpVarHasData", true); // tell parent to enable controls
      } else {
        vm.variable.step = null; // bounds are null => no data for the var
        vm.$emit("updateInterpVarHasData", false); // tell parent to disable controls
      }

      // reset clipping plane normals and inputs
      vm.clipPlanes.x.normal = new THREE.Vector3(1, 0, 0);
      vm.clipPlanes.y.normal = new THREE.Vector3(0, -1, 0);
      vm.clipPlanes.z.normal = new THREE.Vector3(0, 0, -1);

      // reset clipping plane constants
      vm.clipPlanes.x.constant =
        -Math.sign(vm.clipPlanes.x.normal.x) * vm.clipPlanes.x.bounds[0] + 0.01;
      vm.clipPlanes.y.constant =
        Math.sign(vm.clipPlanes.y.normal.y) * -vm.clipPlanes.y.bounds[0] + 0.01;
      vm.clipPlanes.z.constant =
        Math.sign(vm.clipPlanes.z.normal.z) * vm.clipPlanes.z.bounds[0] + 0.01;

      // set clipping plane values to min boundary to start
      vm.clipPlanes.x.value = vm.clipPlanes.x.bounds[0];
      vm.clipPlanes.y.value = vm.clipPlanes.y.bounds[0];
      vm.clipPlanes.z.value = vm.clipPlanes.z.bounds[0];

      // reset clipping plane helpers
      // vm.xClipPlaneHelperVisible = false; // set flag
      // vm.clipPlanes.x.helper.visible = false; // set state
      // vm.yClipPlaneHelperVisible = false; // set flag
      // vm.clipPlanes.y.helper.visible = false; // set state
      // vm.zClipPlaneHelperVisible = false; // set flag
      // vm.clipPlanes.z.helper.visible = false; // set state

      // reset global clip planes
      // vm.clipPlanes.x.global = false;
      // vm.clipPlanes.y.global = false;
      // vm.clipPlanes.z.global = false;
      // vm.renderer.clippingPlanes = Object.freeze([]);

      // reset gridhelper
      // vm.gridHelperVisible = false; // set flag
      // vm.gridHelper.visible = false; // set state
      // vm.gridHelper.position.y = 0; // set position

      // tell parent if options reset
      if (vm.showValues !== true) {
        vm.$emit("updateShowValues", true); // reset to default value
      }
      if (vm.geoHeight !== 1) {
        vm.$emit("updateGeoHeight", 1); // default value, in cm
      }

      vm.clean(); // have to remove old stuff
    },

    clean() {
      let vm = this;

      // dispose of all objects in the scene not named below
      const dontRemove = [
        "gridHelper",
        "axesHelper",
        "frustumHelper",
        "xClipPlaneHelper",
        "yClipPlaneHelper",
        "zClipPlaneHelper",
      ];
      const lines = [];
      const meshes = [];
      vm.scene.traverse(function (object) {
        if (dontRemove.indexOf(object.name) == -1) {
          if (object.isLine) {
            lines.push(object);
          } else if (object.isMesh) {
            meshes.push(object);
          }
        }
      });
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        line.material.dispose();
        line.geometry.dispose();
        vm.scene.remove(line);
      }
      for (let i = 0; i < meshes.length; i++) {
        const mesh = meshes[i];
        mesh.material.dispose();
        mesh.geometry.dispose();
        vm.scene.remove(mesh);
      }

      // add new objects and re-render
      vm.addObjects();
      vm.requestRenderIfNotRequested();
    },

    cleanLimited: throttle(
      function () {
        this.clean();
      },
      200,
      { leading: false }
    ),

    requestRenderIfNotRequested() {
      let vm = this;
      if (!vm.renderRequested) {
        vm.renderRequested = true;
        requestAnimationFrame(vm.render);
      }
    },

    resizeRendererToDisplaySize() {
      let vm = this;
      const pixelRatio = window.devicePixelRatio;
      const width = (vm.canvas.clientWidth * pixelRatio) | 0;
      const height = (vm.canvas.clientHeight * pixelRatio) | 0;
      const needResize =
        vm.canvas.width !== width || vm.canvas.height !== height;
      if (needResize) vm.renderer.setSize(width, height, false);
      return needResize;
    },

    updateMouse(e) {
      // update mouse position relative to the canvas position on the client
      const rect = e.target.getBoundingClientRect();
      this.mouse.x =
        ((e.clientX - rect.left) / (rect.right - rect.left)) * 2 - 1;
      this.mouse.y =
        -((e.clientY - rect.top) / (rect.bottom - rect.top)) * 2 + 1;
    },

    onMouseMove(e) {
      e.preventDefault();
      let vm = this;
      if (vm.mouseMode == "Select") {
        vm.updateMouse(e);
        vm.requestRenderIfNotRequested();
      }
    },

    onClick(e) {
      e.preventDefault();
      let vm = this;
      if (vm.mouseMode == "Select") {
        // find out if the mouse is intersecting anything
        vm.updateMouse(e);
        vm.raycaster.setFromCamera(vm.mouse, vm.camera);
        const instancedMesh = vm.objects[0];
        const intersection = vm.raycaster.intersectObject(instancedMesh);
        if (intersection.length > 0) {
          // get data from the hovered column and save to drawer
          const idx = intersection[0].instanceId; // get hovered point's index
          const currZ = vm.interpData[idx].Z; // get height of hovered point
          const zMin = vm.bounds.z[0];
          const zMax = vm.bounds.z[1];
          const vMin = vm.bounds[vm.variable.name][0];
          const vMax = vm.bounds[vm.variable.name][1];

          // gather list of points in the clicked column
          let pointList = [];
          for (let i = zMin - currZ; i < zMax - currZ + 1; i++) {
            const dataPoint = vm.interpData[idx + i];
            // add variable value as percent to the data point object
            if (vm.variableHasData) {
              const v = dataPoint[vm.variable.name];
              const vPrct = (v - vMin) / (vMax - vMin);
              dataPoint[`${vm.variable.name}_prct`] = vPrct;
            } else {
              dataPoint[`${vm.variable.name}_prct`] = null;
            }
            pointList.push(dataPoint);
          }
          vm.$emit("updateSavedSamples", {
            data: pointList,
            bounds: vm.bounds[vm.variable.name],
          });

          // reset to Orbit controls
          const craneMesh = vm.objects[1];
          craneMesh.visible = false;
          craneMesh.position.set(vm.resolution / 2, 3, vm.resolution / 2);
          const hoverLines = vm.objects[2];
          hoverLines.visible = false;
          hoverLines.position.set(
            vm.resolution / 2,
            (-vm.geoHeight * (vm.bounds.z[1] + 1)) / 2,
            vm.resolution / 2
          );
          vm.$emit("updateInterpMouseMode", "Orbit");
          vm.requestRenderIfNotRequested();
        }
      }
    },

    render() {
      let vm = this;
      vm.renderRequested = false;

      if (vm.mouseMode == "Select") {
        const craneMesh = vm.objects[1];
        const hoverLines = vm.objects[2];

        // find what the mouse is hovering on
        vm.raycaster.setFromCamera(vm.mouse, vm.camera);
        const instancedMesh = vm.objects[0];
        const intersection = vm.raycaster.intersectObject(instancedMesh);
        if (intersection.length > 0) {
          // update visibility and position of the crane and hover lines
          const d = vm.interpData[intersection[0].instanceId]; // get hovered data point
          craneMesh.visible = true;
          craneMesh.position.set(
            d.X + vm.resolution / 2,
            3,
            -(d.Y + vm.resolution / 2)
          );
          hoverLines.visible = true;
          hoverLines.position.set(
            d.X + vm.resolution / 2,
            (-vm.geoHeight * (vm.bounds.z[1] + 1)) / 2,
            -(d.Y + vm.resolution / 2)
          );
        } else {
          // hide the crane and hover lines
          craneMesh.visible = false;
          hoverLines.visible = false;
        }
      }

      // resize the screen if needed
      if (vm.resizeRendererToDisplaySize()) {
        vm.camera.aspect = vm.canvas.clientWidth / vm.canvas.clientHeight;
        vm.camera.updateProjectionMatrix();
      }

      // render the scene
      vm.controls.update();
      vm.renderer.render(vm.scene, vm.camera);
    },
  },
};
</script>

<style scoped>
#interp-container {
  background: #121212;
}

#canvas-container {
  /** 
   * 100 view height -
   * 3 x 64px areas -
   * 1 x 48px area -
   * 100px margins and padding
   */
  width: 100%;
  height: calc(100vh - 3 * (56px) - 48px - 100px);
}

#cvs {
  width: 100%;
  height: 100%;
}

#interp-top-controls-container,
#interp-bottom-controls-container {
  height: 56px;
}

#right-controls-container {
  width: 56px;
}

.slider-border {
  border: 1px solid grey;
  border-radius: 4px;
}

.value-slider >>> .v-slider__track-container {
  height: 4px;
  border-radius: 4px;
  background: var(--bg-gradient) !important;
}

.value-slider >>> .v-slider__track-fill {
  background: none !important;
}

.depth-slider-label {
  height: 1.5rem;
  text-align: center;
}

.depth-slider >>> .v-slider {
  /** 
   * 100 view height -
   * 3 x 56px areas -
   * 1 x 24px text -
   * 1 x 20px buttons -
   * 136px margins and padding
   */
  height: calc(100vh - 3 * (56px) - 24px - 20px - 184px);
  margin-bottom: 0;
}

/* .depth-slider >>> .v-slider__thumb::before {
  left: -9px;
} */

/* .depth-slider >>> .v-slider__thumb {
  width: 18px;
  left: -9px;
} */
</style>
