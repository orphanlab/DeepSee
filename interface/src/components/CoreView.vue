<template>
  <v-container fluid id="core-container" style="overflow: auto">
    <!-- NO DATA -->
    <v-row v-if="!showData">
      <v-card>
        <v-card-title>Loading ...</v-card-title>
      </v-card>
    </v-row>

    <!-- SHOW DATA -->
    <v-row v-if="showData" class="flex-nowrap pa-3">
      <!-- COLUMNS -->
      <v-col
        v-for="(coreName, i) in cylinders"
        :key="i"
        cols="auto"
        class="custom-core-column pa-3"
      >
        <v-card>
          <!-- CORE NAME AND CLEAR -->
          <v-card-title class="ft-md">
            <span>{{ coreName }}</span>
            <v-btn
              icon
              class="custom-clear-btn ml-2"
              @click="removeCylinder(i)"
            >
              <v-icon>{{ icons.mdiClose }}</v-icon>
            </v-btn>
          </v-card-title>

          <!-- CORE DETAILS -->
          <v-card-subtitle class="ft-sm">
            <span>Type: {{ cylinderList[coreName].Type }}</span>
            <br />
            <span>Date: {{ cylinderList[coreName].Date }}</span>
            <br />
          </v-card-subtitle>

          <!-- DATA BARS -->
          <v-container fluid class="px-4 pb-4 pt-0 ft-sm">
            <!-- HAS DATA -->
            <template
              v-if="getFilteredDataPoints(prepared[coreName]).length > 0"
            >
              <!-- HEADER -->
              <v-row class="my-2 mx-0">
                <v-col class="pa-0">Horizon</v-col>
                <v-spacer></v-spacer>
                <v-col class="pa-0 text-right">Value</v-col>
              </v-row>

              <!-- CONTENT -->
              <v-row
                v-for="(dataPoint, j) in getFilteredDataPoints(
                  prepared[coreName]
                )"
                :key="j"
                class="my-2 mx-0"
              >
                <v-col cols="auto" class="pa-0" style="width: 32px">
                  {{ dataPoint.Horizon }}
                </v-col>
                <v-col
                  cols="auto"
                  class="pa-0 mx-2"
                  :style="{
                    width: '64px',
                    background: getLinearGradient(dataPoint[variable]),
                  }"
                ></v-col>
                <v-col class="pa-0 text-right">
                  {{ parseFloat(dataPoint[variable]).toFixed(decimals) }}
                </v-col>
              </v-row>
            </template>

            <!-- NO DATA -->
            <template v-else>
              <v-row>
                <v-col cols="12" class="text-center">
                  <span>No data.</span>
                </v-col>
              </v-row>
            </template>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import groupBy from "lodash/groupBy";
import { mdiClose } from "@mdi/js";

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

export default {
  name: "CoreView",

  props: {
    cruiseData: {
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
    newSelectedCylinders: {
      type: Array,
      default: () => [],
    },
    cmap: {
      type: Function,
      default: () => function () {},
    },
  },

  data: () => ({
    // constants
    icons: {
      mdiClose: mdiClose,
    },
    // inputs
    variable: null,
    cylinders: null,
    // data
    decimals: null,
    bounds: null,
    cylinderList: null,
    prepared: null,
    // flags
    showData: false,
  }),

  computed: {
    ableToRender: function () {
      return (
        this.cruiseData.length > 0 &&
        this.variables.length > 0 &&
        this.newSelectedCylinders.length > 0
      );
    },
  },

  mounted: function () {
    let vm = this;
    if (vm.ableToRender) {
      vm.variable = vm.variables[0]; // set variable
      vm.cylinders = vm.newSelectedCylinders; // update cylinder list
      vm.parseData(vm.cruiseData); // parse data
    }
  },

  watch: {
    cruiseData: function (newCruiseData) {
      let vm = this;
      if (vm.ableToRender) {
        vm.showData = false; // show loading screen
        vm.parseData(newCruiseData); // parse data
      }
    },

    variables: function (newVariables) {
      let vm = this;
      if (vm.ableToRender) {
        vm.showData = false; // show loading screen
        vm.variable = newVariables[0]; // set variable
        vm.parseData(vm.cruiseData); // parse data
      }
    },

    newSelectedCylinders: function (newCylinders) {
      let vm = this;
      if (vm.ableToRender) {
        // only update view if incoming list is different from current selection
        const cylindersSorted = vm.cylinders.slice().sort();
        const newCylindersSorted = newCylinders.slice().sort();
        const same =
          cylindersSorted.length === newCylindersSorted.length &&
          cylindersSorted.every(function (value, index) {
            return value === newCylindersSorted[index];
          });
        if (!same) {
          vm.showData = false; // show loading screen
          vm.cylinders = newCylinders; // update cylinder list
          vm.parseData(vm.cruiseData); // parse data
        }
      }
    },
  },

  methods: {
    parseData(newData) {
      let vm = this;

      // filter data for only cylinders of interest
      const filteredData = newData.filter((p) =>
        vm.cylinders.includes(p.Cylinder)
      );

      // create new boundaries data object
      vm.bounds = Object.assign(
        Object.fromEntries(vm.variables.map((x) => [x, [null, null]]))
      );

      // some datasets have missing values for variables
      // walk through until you can set bounds on each variable
      let varSet = vm.variables.map(() => false);
      for (let j = 0; j < filteredData.length; j++) {
        for (let k = 0; k < vm.variables.length; k++) {
          const v = parseFloat(filteredData[j][vm.variables[k]]);
          if (!Number.isNaN(v)) {
            const varBounds = vm.bounds[vm.variables[k]];
            if (!varSet[k]) {
              // unset => set the first value
              varBounds[0] = v;
              varBounds[1] = v;
              varSet[k] = true;
            } else {
              // set => find the max and min
              varBounds[0] = Math.min(varBounds[0], v);
              varBounds[1] = Math.max(varBounds[1], v);
            }
          }
        }
      }

      // check whether variable has data
      const lb = vm.bounds[vm.variable][0];
      const rb = vm.bounds[vm.variable][1];
      if (lb !== null && rb !== null) {
        vm.decimals = Math.max(countDecimals(lb), countDecimals(rb));
        vm.$emit("updateCoreVarHasData", true); // tell parent to enable controls
      } else {
        vm.$emit("updateCoreVarHasData", false); // tell parent to disable controls
      }
      vm.$emit("updateCoreVarBounds", vm.bounds[vm.variable]);

      // create list of data points with only meta columns
      const rawCylinderList = filteredData.map((p) => {
        return {
          Cylinder: p["Cylinder"],
          Type: p["Core Fate"],
          Date: p["Date"],
        };
      });

      // remove duplicate data points by Cylinder name (keep the last one found)
      const filteredCylinderList = [
        ...new Map(rawCylinderList.map((p) => [p.Cylinder, p])).values(),
      ];

      // prepare datasets by grouping by Cylinder name
      vm.cylinderList = Object.assign(
        {},
        ...filteredCylinderList.map((p) => ({ [p.Cylinder]: p }))
      );
      vm.prepared = groupBy(filteredData, (p) => p.Cylinder);

      // let the data render
      vm.showData = true;
    },

    getFilteredDataPoints(data) {
      let vm = this;
      return data.filter((p) => p[vm.variable] !== "");
    },

    removeCylinder(index) {
      let vm = this;
      vm.cylinders.splice(index, 1); // remove clicked core
      vm.$emit("updateSelectedCylinders", vm.cylinders); // send updated list to parent
    },

    getLinearGradient(v) {
      let vm = this;
      const vMin = vm.bounds[vm.variable][0];
      const vMax = vm.bounds[vm.variable][1];
      const vPrct = (v - vMin) / (vMax - vMin);
      return `linear-gradient(
        90deg, 
        transparent ${(1 - vPrct) * 100}%, 
        ${vm.cmap(vPrct)} ${(1 - vPrct) * 100}%, 
        ${vm.cmap(vPrct)} 100%
      )`;
    },
  },
};
</script>

<style>
#core-container {
  height: calc(100vh - 176px);
}

.custom-core-column {
  width: auto;
}

.custom-clear-btn {
  width: 28px !important;
  height: 28px !important;
}
</style>
