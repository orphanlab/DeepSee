<template>
  <v-app>
    <!-- BEFORE CONFIG IS LOADED -->
    <template v-if="!config.loaded">
      <v-container fluid class="fill-height">
        <v-row align-items="center" justify="center">
          <v-card>
            <v-card-title>Loading...</v-card-title>
          </v-card>
        </v-row>
      </v-container>
    </template>

    <!-- AFTER CONFIG IS LOADED -->
    <template v-else>
      <!-- TITLE BAR -->
      <v-app-bar app prominent height="176" class="pa-0">
        <v-container fluid class="px-0">
          <!-- TOP ROW -->
          <v-row>
            <!-- LEFT PANEL -->
            <v-col cols="6" class="pa-0">
              <!-- TABS -->
              <v-tabs grow style="padding-right: 1px">
                <v-tab :ripple="false">Map View</v-tab>
              </v-tabs>

              <!-- CONTENT -->
              <v-row class="pa-3">
                <!-- LOCATION SELECT MENU -->
                <v-col cols="4">
                  <v-menu
                    bottom
                    min-width="600px"
                    :offset-y="true"
                    :close-on-content-click="false"
                  >
                    <!-- MENU PREVIEW -->
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        outlined
                        dense
                        hide-details
                        readonly
                        label="Location"
                        class="location-menu-text-field"
                        v-model="locationMenuText"
                        v-on="on"
                        v-bind="attrs"
                      >
                        <template v-slot:append>
                          <v-icon v-on="on">{{ icons.mdiMenuDown }}</v-icon>
                        </template>
                      </v-text-field>
                    </template>

                    <!-- MENU CONTENTS -->
                    <v-card>
                      <v-container fluid>
                        <v-row>
                          <!-- CRUISE NAME LIST -->
                          <v-col
                            cols="4"
                            :style="{ 'background-color': '#333' }"
                          >
                            <v-list dense :color="'#333'">
                              <v-list-item-group
                                mandatory
                                v-model="cruise.params.nameIndex"
                              >
                                <v-list-item
                                  class="list-item-rounded"
                                  v-for="(item, i) in cruise.opts.names"
                                  :key="i"
                                  @click="cruise.params.name = item"
                                >
                                  <v-list-item-content>
                                    <v-list-item-title
                                      v-text="item"
                                    ></v-list-item-title>
                                  </v-list-item-content>
                                </v-list-item>
                              </v-list-item-group>
                            </v-list>
                          </v-col>

                          <!-- SITE LIST -->
                          <v-col
                            cols="8"
                            :style="{ 'background-color': '#222' }"
                          >
                            <v-list dense :color="'#222'">
                              <v-list-item-group
                                mandatory
                                v-model="cruise.params.siteIndex"
                              >
                                <v-list-item
                                  class="list-item-rounded"
                                  v-for="(item, i) in cruise.opts.sites"
                                  :key="i"
                                  @click="cruise.params.site = item"
                                >
                                  <v-list-item-content>
                                    <v-list-item-title
                                      v-text="item"
                                    ></v-list-item-title>
                                  </v-list-item-content>
                                </v-list-item>
                              </v-list-item-group>
                            </v-list>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card>
                  </v-menu>
                </v-col>

                <!-- DATE RANGE SELECT MENU -->
                <v-col cols="4">
                  <v-menu
                    bottom
                    max-width="600px"
                    :offset-y="true"
                    :close-on-content-click="false"
                  >
                    <!-- MENU PREVIEW -->
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        outlined
                        dense
                        hide-details
                        readonly
                        label="Date Range"
                        class="date-range-menu-text-field"
                        v-model="dateRangeMenuText"
                        v-on="on"
                        v-bind="attrs"
                      >
                        <template v-slot:append>
                          <v-icon v-on="on">{{ icons.mdiMenuDown }}</v-icon>
                        </template>
                      </v-text-field>
                    </template>

                    <!-- MENU CONTENTS -->
                    <v-card>
                      <v-container fluid>
                        <v-row>
                          <!-- START DATE LIST -->
                          <v-col
                            cols="6"
                            :style="{ 'background-color': '#333' }"
                          >
                            <v-list dense :color="'#333'">
                              <v-list-item-group
                                mandatory
                                v-model="cruise.params.startDateIndex"
                              >
                                <v-list-item
                                  class="list-item-rounded"
                                  v-for="(item, i) in cruise.opts.dates"
                                  :key="i"
                                  @click="cruise.params.startDate = item"
                                >
                                  <v-list-item-content>
                                    <v-list-item-title>
                                      {{ getDateFormatted(item) }}
                                    </v-list-item-title>
                                  </v-list-item-content>
                                </v-list-item>
                              </v-list-item-group>
                            </v-list>
                          </v-col>

                          <!-- END DATE LIST -->
                          <v-col
                            cols="6"
                            :style="{ 'background-color': '#222' }"
                          >
                            <v-list dense :color="'#222'">
                              <v-list-item-group
                                mandatory
                                v-model="cruise.params.endDateIndex"
                              >
                                <v-list-item
                                  class="list-item-rounded"
                                  v-for="(item, i) in cruise.opts.dates"
                                  :key="i"
                                  @click="cruise.params.endDate = item"
                                >
                                  <v-list-item-content>
                                    <v-list-item-title>
                                      {{ getDateFormatted(item) }}
                                    </v-list-item-title>
                                  </v-list-item-content>
                                </v-list-item>
                              </v-list-item-group>
                            </v-list>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card>
                  </v-menu>
                </v-col>

                <!-- CORE FATE FILTER MENU -->
                <v-col cols="4">
                  <v-select
                    multiple
                    outlined
                    dense
                    hide-details
                    label="Core Fate"
                    v-model="cruise.params.fatesSelected"
                    :menu-props="{ bottom: true, offsetY: true }"
                    :items="cruise.opts.fates"
                  >
                    <template v-slot:prepend-item>
                      <v-list-item ripple @click="toggleFatesSelectAll">
                        <v-list-item-action>
                          <v-icon>
                            {{ fatesSelectAllIcon }}
                          </v-icon>
                        </v-list-item-action>
                        <v-list-item-content>
                          <v-list-item-title> Select All </v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>
                      <v-divider class="mt-2"></v-divider>
                    </template>
                    <template v-slot:selection="{ item, index }">
                      <span
                        v-if="index === 0"
                        class="custom-text-field-input"
                        :style="{
                          'max-width':
                            cruise.params.fatesSelected.length == 1
                              ? '100%'
                              : 'calc(100% - 28px)',
                        }"
                      >
                        {{ item }}
                      </span>
                      <span
                        v-if="index === 1"
                        class="grey--text text-caption ml-1"
                      >
                        (+{{ cruise.params.fatesSelected.length - 1 }})
                      </span>
                    </template>
                  </v-select>
                </v-col>
              </v-row>
            </v-col>

            <!-- DIVIDER -->
            <v-divider vertical role="presentation"></v-divider>

            <!-- RIGHT PANEL -->
            <v-col cols="6" class="pa-0">
              <!-- TABS -->
              <v-tabs
                grow
                v-model="leftPanelActiveTab"
                style="margin-left: 1px"
              >
                <v-tab>Core View</v-tab>
                <v-tab>Interpolation View</v-tab>
              </v-tabs>

              <!-- CONTENT -->
              <v-tabs-items
                v-model="leftPanelActiveTab"
                style="margin-left: 1px"
              >
                <!-- CORE VIEW TAB -->
                <v-tab-item class="custom-tab-item-header">
                  <v-row class="pa-3">
                    <!-- CORE VIEW ATTRIBUTE SELECT MENU -->
                    <v-col cols="6">
                      <v-menu
                        left
                        bottom
                        v-model="core.flags.attrMenuActive"
                        max-height="400px"
                        :disabled="cylinders.selected.length == 0"
                        :transition="false"
                        :offset-y="true"
                        :close-on-content-click="false"
                      >
                        <!-- MENU PREVIEW -->
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            outlined
                            dense
                            hide-details
                            readonly
                            label="Attribute"
                            v-model="core.params.attrMenuText"
                            v-on="on"
                            v-bind="attrs"
                            :disabled="cylinders.selected.length == 0"
                          >
                            <template v-slot:append>
                              <v-icon v-on="on">{{ icons.mdiMenuDown }}</v-icon>
                            </template>
                          </v-text-field>
                        </template>

                        <!-- MENU CONTENTS -->
                        <v-card>
                          <v-container fluid>
                            <v-row class="flex-nowrap">
                              <!-- CORE VIEW ATTRIBUTE CATEGORY LIST -->
                              <v-col
                                cols="auto"
                                :style="{ 'background-color': '#333' }"
                              >
                                <v-list dense :color="'#333'">
                                  <v-list-item-group
                                    v-model="core.variables.categoryIndex"
                                  >
                                    <v-list-item
                                      class="list-item-rounded"
                                      v-for="(
                                        item, i
                                      ) in core.variables.categories.filter(
                                        (x) => x !== 'Meta'
                                      )"
                                      :key="i"
                                      @click="setCoreViewVariableCategory(item)"
                                    >
                                      <v-list-item-content>
                                        <v-list-item-title
                                          v-text="item"
                                        ></v-list-item-title>
                                      </v-list-item-content>
                                    </v-list-item>
                                  </v-list-item-group>
                                </v-list>
                              </v-col>

                              <!-- CORE VIEW ATTRIBUTE SEARCH + LIST -->
                              <v-col
                                cols="auto"
                                :style="{
                                  'background-color': '#222',
                                  'overflow-y': 'auto',
                                }"
                              >
                                <!-- SEARCH -->
                                <v-text-field
                                  outlined
                                  dense
                                  hide-details
                                  label="Search"
                                  v-model="core.variables.search"
                                ></v-text-field>

                                <!-- LIST -->
                                <v-list dense :color="'#222'">
                                  <v-list-item
                                    class="list-item-rounded"
                                    v-for="(item, i) in core.variables
                                      .allFiltered"
                                    :key="i"
                                    @click="setCoreViewVariable(item)"
                                  >
                                    <v-list-item-content>
                                      <v-list-item-title
                                        v-text="item"
                                      ></v-list-item-title>
                                    </v-list-item-content>
                                  </v-list-item>
                                </v-list>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-card>
                      </v-menu>
                    </v-col>
                  </v-row>
                </v-tab-item>

                <!-- INTERPOLATE VIEW TAB -->
                <v-tab-item class="custom-tab-item-header">
                  <v-row class="pa-3">
                    <!-- INTERP VIEW ATTRIBUTE SELECT MENU -->
                    <v-col cols="6">
                      <v-menu
                        left
                        bottom
                        v-model="interp.flags.attrMenuActive"
                        max-height="400px"
                        :disabled="cylinders.selected.length == 0"
                        :transition="false"
                        :offset-y="true"
                        :close-on-content-click="false"
                      >
                        <!-- MENU PREVIEW -->
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            outlined
                            dense
                            hide-details
                            readonly
                            label="Attribute"
                            v-model="interp.params.attrMenuText"
                            v-on="on"
                            v-bind="attrs"
                            :disabled="cylinders.selected.length == 0"
                          >
                            <template v-slot:append>
                              <v-icon v-on="on">{{ icons.mdiMenuDown }}</v-icon>
                            </template>
                          </v-text-field>
                        </template>

                        <!-- MENU CONTENTS -->
                        <v-card>
                          <v-container fluid>
                            <v-row class="flex-nowrap">
                              <!-- INTERP VIEW ATTRIBUTE CATEGORY LIST -->
                              <v-col
                                cols="auto"
                                :style="{ 'background-color': '#333' }"
                              >
                                <v-list dense :color="'#333'">
                                  <v-list-item-group
                                    v-model="interp.variables.categoryIndex"
                                  >
                                    <v-list-item
                                      class="list-item-rounded"
                                      v-for="(
                                        item, i
                                      ) in interp.variables.categories.filter(
                                        (x) => x !== 'Meta'
                                      )"
                                      :key="i"
                                      @click="
                                        setInterpViewVariableCategory(item)
                                      "
                                    >
                                      <v-list-item-content>
                                        <v-list-item-title
                                          v-text="item"
                                        ></v-list-item-title>
                                      </v-list-item-content>
                                    </v-list-item>
                                  </v-list-item-group>
                                </v-list>
                              </v-col>

                              <!-- INTERP VIEW ATTRIBUTE SEARCH + LIST -->
                              <v-col
                                cols="auto"
                                :style="{
                                  'background-color': '#222',
                                  'overflow-y': 'auto',
                                }"
                              >
                                <!-- SEARCH -->
                                <v-text-field
                                  outlined
                                  dense
                                  hide-details
                                  label="Search"
                                  v-model="interp.variables.search"
                                ></v-text-field>

                                <!-- LIST -->
                                <v-list dense :color="'#222'">
                                  <v-list-item
                                    class="list-item-rounded"
                                    v-for="(item, i) in interp.variables
                                      .allFiltered"
                                    :key="i"
                                    @click="setInterpViewVariable(item)"
                                  >
                                    <v-list-item-content>
                                      <v-list-item-title
                                        v-text="item"
                                      ></v-list-item-title>
                                    </v-list-item-content>
                                  </v-list-item>
                                </v-list>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-card>
                      </v-menu>
                    </v-col>

                    <!-- INTERP METHOD MENU -->
                    <v-col cols="6">
                      <v-menu
                        bottom
                        v-model="interp.flags.methodMenuActive"
                        max-height="400px"
                        :disabled="cylinders.selected.length == 0"
                        :offset-y="true"
                        :close-on-content-click="false"
                      >
                        <!-- MENU PREVIEW -->
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            outlined
                            dense
                            hide-details
                            readonly
                            label="Interpolation Method"
                            v-model="interpMethodMenuText"
                            v-on="on"
                            v-bind="attrs"
                            :disabled="cylinders.selected.length == 0"
                          >
                            <template v-slot:append>
                              <v-icon v-on="on">{{ icons.mdiMenuDown }}</v-icon>
                            </template>
                          </v-text-field>
                        </template>

                        <!-- MENU CONTENTS -->
                        <v-card>
                          <v-container>
                            <v-row>
                              <!-- METHOD LIST -->
                              <v-col
                                cols="6"
                                :style="{ 'background-color': '#333' }"
                              >
                                <v-card :color="'#333'" elevation="0">
                                  <v-card-title
                                    class="ft-lg pa-0 justify-center"
                                  >
                                    <span>Algorithm</span>
                                  </v-card-title>
                                </v-card>
                                <v-list dense :color="'#333'">
                                  <v-list-item-group
                                    mandatory
                                    v-model="interp.params.methodIndex"
                                  >
                                    <v-list-item
                                      class="list-item-rounded"
                                      v-for="(item, i) in interp.opts.methods"
                                      :key="i"
                                      @click="setInterpMethod(item)"
                                    >
                                      <v-list-item-content>
                                        <v-list-item-title
                                          v-text="item"
                                        ></v-list-item-title>
                                      </v-list-item-content>
                                    </v-list-item>
                                  </v-list-item-group>
                                </v-list>
                              </v-col>

                              <!-- RESOLUTION LIST -->
                              <v-col
                                cols="6"
                                :style="{ 'background-color': '#222' }"
                              >
                                <v-card :color="'#222'" elevation="0">
                                  <v-card-title
                                    class="ft-lg pa-0 justify-center"
                                  >
                                    <span>Grid Size</span>
                                  </v-card-title>
                                </v-card>
                                <v-list dense :color="'#222'">
                                  <v-list-item
                                    class="list-item-rounded"
                                    v-for="(item, i) in interp.opts.resolutions"
                                    :key="i"
                                    @click="setInterpResolution(item)"
                                  >
                                    <v-list-item-content>
                                      <v-list-item-title>
                                        <span>{{ item }}cm</span>
                                      </v-list-item-title>
                                    </v-list-item-content>
                                  </v-list-item>
                                </v-list>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-card>
                      </v-menu>
                    </v-col>
                  </v-row>
                </v-tab-item>
              </v-tabs-items>
            </v-col>
          </v-row>

          <!-- BOTTOM ROW -->
          <v-row class="mt-1" style="height: 72px">
            <!-- LEFT PANEL -->
            <v-col cols="6">
              <v-row>
                <v-col cols="8">
                  <v-row>
                    <!-- MAP CONTROLS -->
                    <v-col cols="5">
                      <div
                        class="
                          v-input
                          v-input--hide-details
                          v-input--is-label-active
                          v-input--is-dirty
                          v-input--is-readonly
                          v-input--dense
                          theme--dark
                          v-text-field
                          v-text-field--is-booted
                          v-text-field--enclosed
                          v-text-field--outlined
                        "
                      >
                        <div class="v-input__control">
                          <div class="v-input__slot">
                            <fieldset
                              aria-hidden="true"
                              class="v-text-field--outlined"
                              style="height: 54px"
                            >
                              <legend style="width: 78px">
                                <span class="notranslate"
                                  >&ZeroWidthSpace;</span
                                >
                              </legend>
                            </fieldset>
                            <div
                              class="v-text-field__slot"
                              style="cursor: default"
                            >
                              <!-- LABEL -->
                              <label
                                class="v-label v-label--active theme--dark"
                                style="
                                  left: 0px;
                                  right: auto;
                                  position: absolute;
                                "
                              >
                                Map Controls
                              </label>

                              <!-- ICONS -->
                              <v-row class="pt-2 px-2" justify="space-around">
                                <!-- UNDO -->
                                <v-col cols="4" class="pa-0 text-center">
                                  <v-btn
                                    small
                                    class="pa-0"
                                    min-width="28px"
                                    elevation="0"
                                    color="#444"
                                    @click="$refs.mapView.undo('Zoom')"
                                  >
                                    <v-icon>{{ icons.mdiUndo }}</v-icon>
                                  </v-btn>
                                </v-col>

                                <!-- REFRESH MAP VIEW -->
                                <v-col cols="4" class="pa-0 text-center">
                                  <v-btn
                                    small
                                    class="pa-0"
                                    min-width="28px"
                                    elevation="0"
                                    color="#444"
                                    @click="resetMapView"
                                  >
                                    <v-icon>{{ icons.mdiRefresh }}</v-icon>
                                  </v-btn>
                                </v-col>

                                <!-- DOWNLOAD -->
                                <v-col cols="4" class="pa-0 text-center">
                                  <v-btn
                                    disabled
                                    small
                                    class="pa-0"
                                    min-width="28px"
                                    elevation="0"
                                    color="#444"
                                  >
                                    <v-icon>{{ icons.mdiDownload }}</v-icon>
                                  </v-btn>
                                </v-col>
                              </v-row>
                            </div>
                          </div>
                        </div>
                      </div>
                    </v-col>

                    <!-- ANNOTATE -->
                    <v-col cols="7">
                      <div
                        class="
                          v-input
                          v-input--hide-details
                          v-input--is-label-active
                          v-input--is-dirty
                          v-input--is-readonly
                          v-input--dense
                          theme--dark
                          v-text-field
                          v-text-field--is-booted
                          v-text-field--enclosed
                          v-text-field--outlined
                        "
                      >
                        <div class="v-input__control">
                          <div class="v-input__slot">
                            <fieldset
                              aria-hidden="true"
                              class="v-text-field--outlined"
                              style="height: 54px"
                            >
                              <legend style="width: 54.5px">
                                <span class="notranslate"
                                  >&ZeroWidthSpace;</span
                                >
                              </legend>
                            </fieldset>
                            <div
                              class="v-text-field__slot"
                              style="cursor: default"
                            >
                              <!-- LABEL -->
                              <label
                                class="v-label v-label--active theme--dark"
                                style="
                                  left: 0px;
                                  right: auto;
                                  position: absolute;
                                "
                              >
                                Annotate
                              </label>

                              <!-- ICONS -->
                              <v-row class="pt-2 px-2" justify="space-around">
                                <!-- DRAW -->
                                <v-col class="pa-0 text-center custom-cols-5">
                                  <v-btn
                                    small
                                    class="pa-0"
                                    min-width="28px"
                                    elevation="0"
                                    :color="
                                      map.params.dragMode == 'Draw'
                                        ? 'primary'
                                        : '#444'
                                    "
                                    @click="
                                      map.params.dragMode =
                                        map.params.dragMode == 'Draw'
                                          ? 'Zoom'
                                          : 'Draw'
                                    "
                                  >
                                    <v-icon>{{ icons.mdiPencil }}</v-icon>
                                  </v-btn>
                                </v-col>

                                <!-- COLOR -->
                                <v-col class="pa-0 text-center custom-cols-5">
                                  <v-menu
                                    bottom
                                    :offset-y="true"
                                    :close-on-content-click="true"
                                  >
                                    <!-- MENU PREVIEW -->
                                    <template v-slot:activator="{ on, attrs }">
                                      <v-btn
                                        small
                                        class="pa-0"
                                        min-width="28px"
                                        elevation="0"
                                        color="#444"
                                        v-on="on"
                                        v-bind="attrs"
                                      >
                                        <v-icon
                                          v-on="on"
                                          :style="{
                                            color:
                                              map.opts.dragColors[
                                                map.params.dragColor
                                              ].background,
                                          }"
                                        >
                                          {{ icons.mdiPalette }}
                                        </v-icon>
                                      </v-btn>
                                    </template>

                                    <!-- MENU CONTENTS -->
                                    <v-card
                                      :style="{ 'background-color': '#333' }"
                                    >
                                      <v-container fluid>
                                        <v-list
                                          dense
                                          :color="'#333'"
                                          class="py-0"
                                        >
                                          <v-list-item-group
                                            mandatory
                                            v-model="map.params.dragColorIndex"
                                          >
                                            <v-list-item
                                              v-for="(item, i) in Object.keys(
                                                map.opts.dragColors
                                              )"
                                              :key="i"
                                              class="list-item-rounded my-2"
                                              :style="{
                                                'background-color':
                                                  map.opts.dragColors[item]
                                                    .background,
                                              }"
                                              @click="
                                                map.params.dragColor = item
                                              "
                                            >
                                              <v-list-item-content>
                                                <v-list-item-title
                                                  v-text="
                                                    item.replace('_', ' ')
                                                  "
                                                  :style="{
                                                    color:
                                                      map.opts.dragColors[item]
                                                        .text,
                                                  }"
                                                ></v-list-item-title>
                                              </v-list-item-content>
                                            </v-list-item>
                                          </v-list-item-group>
                                        </v-list>
                                      </v-container>
                                    </v-card>
                                  </v-menu>
                                </v-col>

                                <!-- UNDO -->
                                <v-col class="pa-0 text-center custom-cols-5">
                                  <v-btn
                                    small
                                    class="pa-0"
                                    min-width="28px"
                                    elevation="0"
                                    color="#444"
                                    @click="$refs.mapView.undo('Draw')"
                                  >
                                    <v-icon>{{ icons.mdiUndo }}</v-icon>
                                  </v-btn>
                                </v-col>

                                <!-- REDO -->
                                <v-col class="pa-0 text-center custom-cols-5">
                                  <v-btn
                                    disabled
                                    small
                                    class="pa-0"
                                    min-width="28px"
                                    elevation="0"
                                    color="#444"
                                    @click="$refs.mapView.redoDrawing()"
                                  >
                                    <v-icon>{{ icons.mdiRedo }}</v-icon>
                                  </v-btn>
                                </v-col>

                                <!-- DELETE -->
                                <v-col class="pa-0 text-center custom-cols-5">
                                  <v-btn
                                    small
                                    class="pa-0"
                                    min-width="28px"
                                    elevation="0"
                                    color="#444"
                                    @click="$refs.mapView.deleteDrawing()"
                                  >
                                    <v-icon>{{ icons.mdiDelete }}</v-icon>
                                  </v-btn>
                                </v-col>
                              </v-row>
                            </div>
                          </div>
                        </div>
                      </div>
                    </v-col>
                  </v-row>
                </v-col>

                <!-- SELECTED RANGE -->
                <v-col cols="4">
                  <div
                    class="
                      v-input
                      v-input--hide-details
                      v-input--is-label-active
                      v-input--is-dirty
                      v-input--is-readonly
                      v-input--dense
                      theme--dark
                      v-text-field
                      v-text-field--is-booted
                      v-text-field--enclosed
                      v-text-field--outlined
                    "
                  >
                    <div class="v-input__control">
                      <div class="v-input__slot">
                        <fieldset
                          aria-hidden="true"
                          class="v-text-field--outlined"
                          style="height: 54px"
                        >
                          <legend style="width: 88.5px">
                            <span class="notranslate">&ZeroWidthSpace;</span>
                          </legend>
                        </fieldset>
                        <div class="v-text-field__slot" style="cursor: default">
                          <!-- LABEL -->
                          <label
                            class="v-label v-label--active theme--dark"
                            style="left: 0px; right: auto; position: absolute"
                          >
                            Selected Range
                          </label>

                          <!-- ICONS -->
                          <v-row class="pt-2 px-3">
                            <!-- LABEL -->
                            <v-col
                              cols="auto"
                              class="pa-0"
                              style="max-width: calc(100% - 64px)"
                              align-self="center"
                            >
                              <span
                                v-if="
                                  map.params.dragMode !== 'Select' &&
                                  cylinders.selected.length == 0
                                "
                                class="custom-text-field-input"
                              >
                                Unselected
                              </span>
                              <span
                                v-if="map.params.dragMode == 'Select'"
                                class="custom-text-field-input"
                              >
                                Click and Drag below
                              </span>
                              <span
                                v-if="
                                  map.params.dragMode !== 'Select' &&
                                  cylinders.selected.length > 0
                                "
                                class="custom-text-field-input"
                              >
                                Selected
                              </span>
                            </v-col>

                            <!-- SPACER -->
                            <v-spacer></v-spacer>

                            <!-- DRAG MODE TOGGLE -->
                            <v-col cols="auto" class="pa-0 pr-2 text-center">
                              <v-btn
                                small
                                class="pa-0"
                                min-width="28px"
                                elevation="0"
                                :color="
                                  map.params.dragMode == 'Select'
                                    ? 'primary'
                                    : '#444'
                                "
                                @click="
                                  map.params.dragMode =
                                    map.params.dragMode == 'Select'
                                      ? 'Zoom'
                                      : 'Select'
                                "
                              >
                                <v-icon>{{ icons.mdiCrosshairs }}</v-icon>
                              </v-btn>
                            </v-col>

                            <!-- CLEAR SELECTED CYLINDERS -->
                            <v-col cols="auto" class="pa-0 text-center">
                              <v-btn
                                small
                                class="pa-0"
                                min-width="28px"
                                elevation="0"
                                :color="'#444'"
                                @click="updateSelectedCylinders([])"
                              >
                                <v-icon>{{ icons.mdiClose }}</v-icon>
                              </v-btn>
                            </v-col>
                          </v-row>
                        </div>
                      </div>
                    </div>
                  </div>
                </v-col>
              </v-row>
            </v-col>

            <!-- DIVIDER -->
            <v-divider vertical role="presentation"></v-divider>

            <!-- RIGHT PANEL -->
            <v-col cols="6" class="pa-0">
              <v-tabs-items
                v-model="leftPanelActiveTab"
                style="margin-left: 1px"
              >
                <!-- CORE VIEW TAB -->
                <v-tab-item class="custom-tab-item-header" style="height: 72px">
                  <v-row class="pa-3">
                    <!-- COLOR MODE MENU -->
                    <v-col cols="4">
                      <v-menu
                        bottom
                        :disabled="!(showCoreView && core.variables.hasData)"
                        :offset-y="true"
                        :close-on-content-click="true"
                      >
                        <!-- MENU PREVIEW -->
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            outlined
                            dense
                            hide-details
                            readonly
                            label="Color Mode"
                            height="49px"
                            v-model="coreViewColorModeMenuText"
                            v-on="on"
                            v-bind="attrs"
                            :disabled="
                              !(showCoreView && core.variables.hasData)
                            "
                          >
                            <template v-slot:append>
                              <v-icon v-on="on">{{ icons.mdiMenuDown }}</v-icon>
                            </template>
                          </v-text-field>
                        </template>

                        <!-- MENU CONTENTS -->
                        <v-card>
                          <v-container fluid class="pb-0">
                            <!-- COLOR MODE LIST -->
                            <v-row no-gutters>
                              <v-col cols="12" class="py-0">
                                <v-list dense>
                                  <v-list-item
                                    v-for="(item, i) in Object.keys(
                                      core.opts.cmaps
                                    )"
                                    :key="i"
                                    class="list-item-rounded my-2"
                                    :style="{
                                      background: getCMapLinearGradient(
                                        core.opts.cmaps[item].func
                                      ),
                                    }"
                                    @click="core.params.cmap = item"
                                  >
                                    <v-list-item-content>
                                      <v-list-item-title
                                        v-text="item"
                                        :style="{
                                          color: core.opts.cmaps[item].text,
                                        }"
                                      >
                                      </v-list-item-title>
                                    </v-list-item-content>
                                  </v-list-item>
                                </v-list>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-card>
                      </v-menu>
                    </v-col>

                    <!-- CORE VIEW COLOR BAR -->
                    <v-col
                      v-if="showCoreView && core.variables.hasData"
                      cols="8"
                    >
                      <div
                        class="core-view-color-bar"
                        :style="{
                          background: getCMapLinearGradient(
                            core.opts.cmaps[core.params.cmap].func
                          ),
                        }"
                      ></div>
                      <v-row class="core-view-bounds ft-lg">
                        <v-col cols="auto" class="pa-0">
                          {{ core.params.varBounds[0] }}
                        </v-col>
                        <v-spacer></v-spacer>
                        <v-col cols="auto" class="pa-0">
                          {{ core.params.varBounds[1] }}
                        </v-col>
                      </v-row>
                    </v-col>
                  </v-row>
                </v-tab-item>

                <!-- INTERPOLATION VIEW TAB -->
                <v-tab-item class="custom-tab-item-header">
                  <v-row class="pa-3">
                    <!-- COLOR MODE MENU -->
                    <v-col cols="4">
                      <v-menu
                        bottom
                        :disabled="
                          !interp.flags.viewActive || !interp.variables.hasData
                        "
                        :offset-y="true"
                        :close-on-content-click="false"
                      >
                        <!-- MENU PREVIEW -->
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            outlined
                            dense
                            hide-details
                            readonly
                            label="Color Mode"
                            height="49px"
                            v-model="interpViewColorModeMenuText"
                            v-on="on"
                            v-bind="attrs"
                            :disabled="
                              !interp.flags.viewActive ||
                              !interp.variables.hasData
                            "
                          >
                            <template v-slot:append>
                              <v-icon v-on="on">{{ icons.mdiMenuDown }}</v-icon>
                            </template>
                          </v-text-field>
                        </template>

                        <!-- MENU CONTENTS -->
                        <v-card>
                          <v-container fluid class="pb-0">
                            <!-- MODE TOGGLE -->
                            <v-row>
                              <v-col cols="12" class="text-center">
                                <v-btn-toggle
                                  borderless
                                  mandatory
                                  v-model="interp.params.colorModeIndex"
                                >
                                  <!-- STANDARD -->
                                  <v-btn
                                    elevation="0"
                                    color="#444"
                                    @click="setInterpColorMode('Standard')"
                                  >
                                    <span class="hidden-sm-and-down"
                                      >Standard</span
                                    >
                                  </v-btn>

                                  <!-- UNCERTAINTY -->
                                  <v-btn
                                    elevation="0"
                                    color="#444"
                                    @click="setInterpColorMode('Uncertainty')"
                                  >
                                    <span class="hidden-sm-and-down"
                                      >Uncertainty</span
                                    >
                                  </v-btn>
                                </v-btn-toggle>
                              </v-col>
                            </v-row>

                            <!-- COLOR PALETTE LEGEND -->
                            <v-row no-gutters>
                              <svg
                                id="color-mode-legend"
                                width="240"
                                :height="interp.params.colorModeLegendHeight"
                              ></svg>
                            </v-row>

                            <!-- COLOR MODE LIST -->
                            <v-row no-gutters>
                              <v-col cols="12" class="py-0">
                                <v-list dense>
                                  <v-list-item
                                    v-for="(item, i) in Object.keys(
                                      interp.opts.cmaps
                                    )"
                                    :key="i"
                                    class="list-item-rounded my-2"
                                    :style="{
                                      background: getCMapLinearGradient(
                                        interp.opts.cmaps[item].func
                                      ),
                                    }"
                                    @click="interp.params.cmap = item"
                                  >
                                    <v-list-item-content>
                                      <v-list-item-title
                                        v-text="item"
                                        :style="{
                                          color: interp.opts.cmaps[item].text,
                                        }"
                                      >
                                      </v-list-item-title>
                                    </v-list-item-content>
                                  </v-list-item>
                                </v-list>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-card>
                      </v-menu>
                    </v-col>

                    <!-- VIEW CONTROLS -->
                    <v-col cols="4">
                      <div
                        class="
                          v-input
                          v-input--hide-details
                          v-input--is-label-active
                          v-input--is-dirty
                          v-input--is-readonly
                          v-input--dense
                          theme--dark
                          v-text-field
                          v-text-field--is-booted
                          v-text-field--enclosed
                          v-text-field--outlined
                        "
                      >
                        <div class="v-input__control">
                          <div class="v-input__slot">
                            <fieldset
                              aria-hidden="true"
                              class="v-text-field--outlined"
                              style="height: 54px"
                            >
                              <legend style="width: 80px">
                                <span class="notranslate"
                                  >&ZeroWidthSpace;</span
                                >
                              </legend>
                            </fieldset>
                            <div
                              class="v-text-field__slot"
                              style="cursor: default"
                            >
                              <!-- LABEL -->
                              <label
                                class="v-label v-label--active theme--dark"
                                style="
                                  left: 0px;
                                  right: auto;
                                  position: absolute;
                                "
                              >
                                View Controls
                              </label>

                              <!-- ICONS -->
                              <v-row class="pt-2 px-2" justify="space-around">
                                <!-- INTERPOLATION TOGGLE -->
                                <v-col cols="3" class="pa-0 text-center">
                                  <v-btn
                                    small
                                    class="pa-0"
                                    min-width="28px"
                                    elevation="0"
                                    :disabled="
                                      !interp.flags.viewActive ||
                                      !interp.variables.hasData
                                    "
                                    :color="
                                      interp.params.showValues
                                        ? 'primary'
                                        : '#444'
                                    "
                                    @click="
                                      interp.params.showValues =
                                        !interp.params.showValues
                                    "
                                  >
                                    <v-icon>{{ icons.mdiEye }}</v-icon>
                                  </v-btn>
                                </v-col>

                                <!-- SHAPE TOGGLE -->
                                <v-col cols="3" class="pa-0 text-center">
                                  <v-btn
                                    small
                                    class="pa-0"
                                    min-width="28px"
                                    elevation="0"
                                    color="#444"
                                    :disabled="
                                      !interp.flags.viewActive ||
                                      !interp.variables.hasData
                                    "
                                    @click="toggleShapeType"
                                  >
                                    <v-icon
                                      v-if="interp.params.shapeType == 'Prism'"
                                    >
                                      {{ icons.mdiCube }}
                                    </v-icon>
                                    <v-icon
                                      v-if="
                                        interp.params.shapeType == 'Cylinder'
                                      "
                                      class="cylinder-icon"
                                    >
                                      $cylinder
                                    </v-icon>
                                  </v-btn>
                                </v-col>

                                <!-- HEIGHT TOGGLE -->
                                <v-col cols="3" class="pa-0 text-center">
                                  <v-btn
                                    small
                                    class="pa-0"
                                    min-width="28px"
                                    elevation="0"
                                    :disabled="
                                      !interp.flags.viewActive ||
                                      !interp.variables.hasData
                                    "
                                    :color="
                                      interp.params.geoHeight > 1
                                        ? 'primary'
                                        : '#444'
                                    "
                                    @click="setGeoHeight(true)"
                                  >
                                    <v-icon>{{
                                      icons.mdiArrowExpandVertical
                                    }}</v-icon>
                                  </v-btn>
                                </v-col>

                                <!-- REFRESH INTERPOLATION VIEW -->
                                <v-col cols="3" class="pa-0 text-center">
                                  <v-btn
                                    small
                                    class="pa-0"
                                    min-width="28px"
                                    elevation="0"
                                    color="#444"
                                    :disabled="
                                      !interp.flags.viewActive ||
                                      !interp.variables.hasData
                                    "
                                    @click="$refs.interpView.resetView()"
                                  >
                                    <v-icon>{{ icons.mdiRefresh }}</v-icon>
                                  </v-btn>
                                </v-col>
                              </v-row>
                            </div>
                          </div>
                        </div>
                      </div>
                    </v-col>

                    <!-- SELECT A CORE -->
                    <v-col cols="4">
                      <div
                        class="
                          v-input
                          v-input--hide-details
                          v-input--is-label-active
                          v-input--is-dirty
                          v-input--is-readonly
                          v-input--dense
                          theme--dark
                          v-text-field
                          v-text-field--is-booted
                          v-text-field--enclosed
                          v-text-field--outlined
                        "
                      >
                        <div class="v-input__control">
                          <div class="v-input__slot">
                            <fieldset
                              aria-hidden="true"
                              class="v-text-field--outlined"
                              style="height: 54px"
                            >
                              <legend style="width: 80px">
                                <span class="notranslate"
                                  >&ZeroWidthSpace;</span
                                >
                              </legend>
                            </fieldset>
                            <div
                              class="v-text-field__slot"
                              style="cursor: default"
                            >
                              <!-- LABEL -->
                              <label
                                class="v-label v-label--active theme--dark"
                                style="
                                  left: 0px;
                                  right: auto;
                                  position: absolute;
                                "
                              >
                                Selected Core
                              </label>

                              <!-- ICONS -->
                              <v-row class="pt-2 px-3">
                                <!-- LABEL -->
                                <v-col
                                  cols="auto"
                                  class="pa-0"
                                  style="max-width: calc(100% - 64px)"
                                  align-items="end"
                                >
                                  <span
                                    v-if="interp.params.mouseMode == 'Orbit'"
                                    class="custom-text-field-input"
                                  >
                                    <template
                                      v-if="cylinders.saved.length == 0"
                                    >
                                      No saved cores
                                    </template>
                                    <template
                                      v-if="cylinders.saved.length == 1"
                                    >
                                      {{ cylinders.saved.length }} saved core
                                    </template>
                                    <template v-if="cylinders.saved.length > 1">
                                      {{ cylinders.saved.length }} saved cores
                                    </template>
                                  </span>
                                  <span
                                    v-if="interp.params.mouseMode == 'Select'"
                                    class="custom-text-field-input"
                                  >
                                    Click below to save
                                  </span>
                                </v-col>

                                <!-- SPACER -->
                                <v-spacer></v-spacer>

                                <!-- SELECT -->
                                <v-col cols="auto" class="pa-0 text-center">
                                  <v-btn
                                    small
                                    class="pa-0 mr-1"
                                    min-width="28px"
                                    elevation="0"
                                    :disabled="
                                      !interp.flags.viewActive ||
                                      !interp.variables.hasData
                                    "
                                    :color="
                                      interp.params.mouseMode == 'Select'
                                        ? 'primary'
                                        : '#444'
                                    "
                                    @click="
                                      interp.params.mouseMode =
                                        interp.params.mouseMode == 'Select'
                                          ? 'Orbit'
                                          : 'Select'
                                    "
                                  >
                                    <v-icon>{{ icons.mdiHandRight }}</v-icon>
                                  </v-btn>
                                </v-col>
                              </v-row>
                            </div>
                          </div>
                        </div>
                      </div>
                    </v-col>
                  </v-row>
                </v-tab-item>
              </v-tabs-items>
            </v-col>
          </v-row>
        </v-container>
      </v-app-bar>

      <!-- MAIN APP -->
      <v-main>
        <v-container
          fluid
          id="view-area"
          style="max-height: calc(100vh - 128px)"
        >
          <v-row>
            <!-- LEFT PANEL -->
            <v-col cols="6" class="pa-0">
              <!-- MAP VIEW -->
              <MapView
                ref="mapView"
                v-if="map.flags.viewActive"
                :cruise-name="cruise.params.name"
                :cruise-data="cruise.params.data"
                :backgrounds="map.opts.backgrounds"
                :site="cruise.params.site"
                :start-date="cruise.params.startDate"
                :end-date="cruise.params.endDate"
                :fates="cruise.params.fatesSelected"
                :drag-color="
                  map.opts.dragColors[map.params.dragColor].background
                "
                :drag-mode="map.params.dragMode"
                :new-selected-cylinders="cylinders.selected"
                @updateDragMode="updateDragMode"
                @updateSelectedCylinders="updateSelectedCylinders"
              />
            </v-col>

            <!-- RIGHT PANEL -->
            <v-col cols="6" class="pa-0">
              <v-tabs-items v-model="leftPanelActiveTab">
                <!-- CORE VIEW TAB -->
                <v-tab-item class="custom-tab-item-body">
                  <!-- CYLINDER VIEW -->
                  <CoreView
                    ref="coreView"
                    v-if="showCoreView"
                    :cruise-data="cruise.params.data"
                    :variables="core.variables.selected"
                    :variables-changed="core.flags.variablesChanged"
                    :new-selected-cylinders="cylinders.selected"
                    :cmap="core.opts.cmaps[core.params.cmap].func"
                    @updateSelectedCylinders="updateSelectedCylinders"
                    @updateCoreVarHasData="updateCoreVarHasData"
                    @updateCoreVarBounds="updateCoreVarBounds"
                    @resetCoreViewChangedFlags="resetCoreViewChangedFlags"
                  />

                  <!-- OTHER VIEW -->
                  <v-container fluid v-show="!showCoreView" class="fill-height">
                    <v-row align="center" justify="center">
                      <v-card
                        v-if="
                          cylinders.selected.length > 0 &&
                          core.variables.selected.length == 0
                        "
                      >
                        <v-card-title>
                          Select a variable to visualize above.
                        </v-card-title>
                      </v-card>
                      <v-card v-else>
                        <v-card-title>
                          Select cylinders on the left to get started!
                        </v-card-title>
                      </v-card>
                    </v-row>
                  </v-container>
                </v-tab-item>

                <!-- INTERPOLATION TAB VIEW -->
                <v-tab-item class="custom-tab-item-body">
                  <!-- INTERP VIEW -->
                  <InterpView
                    ref="interpView"
                    v-show="interp.flags.viewActive"
                    :interp-data="interp.params.data"
                    :cylinders="cylinders.selected"
                    :variables="interp.variables.selected"
                    :variables-changed="interp.flags.variablesChanged"
                    :resolution="interp.params.resolution"
                    :resolution-changed="interp.flags.resolutionChanged"
                    :color-mode="interp.params.colorMode"
                    :cmap="interp.opts.cmaps[interp.params.cmap].func"
                    :shape-type="interp.params.shapeType"
                    :show-values="interp.params.showValues"
                    :geo-height="interp.params.geoHeight"
                    :mouse-mode="interp.params.mouseMode"
                    @updateSavedSamples="updateSavedSamples"
                    @updateInterpMouseMode="updateInterpMouseMode"
                    @updateInterpVarHasData="updateInterpVarHasData"
                    @updateColorModeLegend="updateColorModeLegend"
                    @resetInterpViewChangedFlags="resetInterpViewChangedFlags"
                  />

                  <!-- OTHER VIEW -->
                  <v-container
                    v-show="!interp.flags.viewActive"
                    fluid
                    class="fill-height"
                  >
                    <v-row align="center" justify="center">
                      <v-card
                        v-show="
                          !interp.flags.viewLoading &&
                          !interp.flags.viewFailed &&
                          !interp.flags.viewNonWindowsDetectedDuringInterp &&
                          cylinders.selected.length == 0
                        "
                      >
                        <v-card-title>
                          Select cylinders on the left to get started!
                        </v-card-title>
                      </v-card>
                      <v-card
                        v-show="
                          !interp.flags.viewLoading &&
                          !interp.flags.viewFailed &&
                          !interp.flags.viewNonWindowsDetectedDuringInterp &&
                          cylinders.selected.length > 0
                        "
                      >
                        <v-card-title>
                          Select both an attribute and interpolation method
                          above.
                        </v-card-title>
                      </v-card>
                      <v-card v-show="interp.flags.viewLoading">
                        <v-card-title>Loading...</v-card-title>
                      </v-card>
                      <v-card v-show="interp.flags.viewFailed">
                        <v-card-title>
                          Request for interpolation from backend failed. Please
                          check the console and server logs for possible errors
                          and try again.
                        </v-card-title>
                      </v-card>
                      <v-card
                        v-show="interp.flags.viewNonWindowsDetectedDuringInterp"
                      >
                        <v-card-title>
                          Natural neighbors interpolation only works on a
                          Windows computer. Please use the Windows version of
                          the tool or try a different interpolation method.
                        </v-card-title>
                      </v-card>
                    </v-row>
                  </v-container>
                </v-tab-item>
              </v-tabs-items>
            </v-col>
          </v-row>
        </v-container>
      </v-main>

      <!-- BOTTOM DRAWER -->
      <v-bottom-navigation
        fixed
        id="bottom-drawer"
        ref="bottomDrawer"
        height="384px"
        scroll-threshold="10000"
        :input-value="bottomDrawerActive"
      >
        <!-- OPEN / CLOSE TAB -->
        <v-card outlined id="bottom-drawer-toggle-card" class="rounded-t-lg">
          <v-btn
            id="bottom-drawer-toggle-btn"
            class="rounded-t-lg"
            :ripple="false"
            @click="bottomDrawerActive = !bottomDrawerActive"
          >
            <v-icon v-if="bottomDrawerActive">{{ icons.mdiMenuDown }}</v-icon>
            <v-icon v-if="!bottomDrawerActive">{{ icons.mdiMenuUp }}</v-icon>
          </v-btn>
        </v-card>

        <!-- DRAWER CONTENT -->
        <v-card id="bottom-drawer-content-card">
          <v-container fluid fill-height class="pa-7">
            <v-row class="flex-nowrap" style="height: 100%">
              <!-- LEFT -->
              <v-col cols="2" class="py-0 px-7">
                <v-list dense :color="'#333'" class="py-0">
                  <!-- EXPORT ALL -->
                  <v-list-item
                    class="list-item-rounded mb-3 text-center"
                    :disabled="cylinders.saved.length == 0"
                    :style="{
                      'background-color': '#727272',
                    }"
                    @click="exportSavedSamples"
                  >
                    <v-list-item-content>
                      <v-list-item-title>Export All</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <!-- CLEAR ALL -->
                  <v-list-item
                    class="list-item-rounded my-3 text-center"
                    :disabled="cylinders.saved.length == 0"
                    :style="{
                      'background-color': '#727272',
                    }"
                    @click="cylinders.saved = []"
                  >
                    <v-list-item-content>
                      <v-list-item-title>Clear All</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-col>

              <!-- DIVIDER -->
              <v-divider vertical role="presentation"></v-divider>

              <!-- RIGHT -->
              <v-col cols="auto" class="py-0 px-7">
                <v-row class="flex-nowrap">
                  <v-col
                    v-for="(item, i) in cylinders.saved"
                    :key="i"
                    cols="auto"
                  >
                    <!-- CARD CONTENTS -->
                    <v-card class="pa-7 ft-sm" style="border-radius: 0">
                      <!-- CLEAR BUTTON -->
                      <v-btn
                        icon
                        absolute
                        top
                        right
                        elevation="8"
                        class="saved-sample-clear-btn"
                        style="color: #272727 !important"
                        @click="cylinders.saved.splice(i, 1)"
                      >
                        <v-icon>{{ icons.mdiClose }}</v-icon>
                      </v-btn>

                      <!-- META INFORMATION -->
                      <div class="pb-2">
                        <span>{{ `${item.cruise} → ${item.site}` }}</span>
                        <br />
                        <span>{{ `Lat: ${item.latitude}` }}</span>
                        <br />
                        <span>{{ `Lon: ${item.longitude}` }}</span>
                        <br />
                        <br />
                        <span>{{ `${item.variable} interpolation` }}</span>
                        <br />
                        <span>
                          {{ `${item.method} at ${item.resolution}cm` }}
                        </span>
                        <br />
                        <span>
                          {{
                            `${item.startDepth}cm - ${item.finalDepth}cm depth`
                          }}
                        </span>
                      </div>

                      <!-- BAR CHART -->
                      <div
                        v-for="(v, j) in getSavedCoreDataBinned(
                          item.data,
                          item.variable
                        )"
                        :key="j"
                        class="pb-2"
                        :style="{
                          margin: '4px 0',
                          height: '6px',
                          background: getSavedCoreLinearGradient(v),
                        }"
                      ></div>

                      <!-- VARIABLE BOUNDS -->
                      <v-row no-gutters justify="space-between">
                        <v-col cols="auto" class="pa-0">
                          <span>
                            {{
                              Math.round(
                                (item.bounds[0] + Number.EPSILON) * 10000
                              ) / 10000
                            }}
                          </span>
                        </v-col>
                        <v-col cols="auto" class="pa-0">
                          <span>
                            {{
                              Math.round(
                                (item.bounds[1] + Number.EPSILON) * 10000
                              ) / 10000
                            }}
                          </span>
                        </v-col>
                      </v-row>
                    </v-card>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-bottom-navigation>
    </template>
  </v-app>
</template>

<script>
import * as csv from "jquery-csv";
import axios from "axios";
import debounce from "lodash/debounce";
import {
  select,
  interpolateViridis,
  interpolateCividis,
  interpolateGreys,
  interpolateInferno,
  interpolatePlasma,
  interpolateMagma,
} from "d3";
import {
  mdiMenuDown,
  mdiCloseBox,
  mdiMinusBox,
  mdiCheckboxBlankOutline,
  mdiUndo,
  mdiRefresh,
  mdiDownload,
  mdiPencil,
  mdiPalette,
  mdiRedo,
  mdiDelete,
  mdiCrosshairs,
  mdiClose,
  mdiEye,
  mdiCube,
  mdiArrowExpandVertical,
  mdiHandRight,
  mdiMenuUp,
} from "@mdi/js";
import MapView from "./components/MapView";
import InterpView from "./components/InterpView";
import CoreView from "./components/CoreView";

export default {
  name: "App",

  components: {
    MapView,
    InterpView,
    CoreView,
  },

  data: () => ({
    // constants
    publicPath: process.env.BASE_URL,
    backendURL: "http://localhost:3000",
    // backendURL: "https://d2d-2021-oceans-backend.herokuapp.com",
    icons: {
      mdiMenuDown: mdiMenuDown,
      mdiCloseBox: mdiCloseBox,
      mdiMinusBox: mdiMinusBox,
      mdiCheckboxBlankOutline: mdiCheckboxBlankOutline,
      mdiUndo: mdiUndo,
      mdiRefresh: mdiRefresh,
      mdiDownload: mdiDownload,
      mdiPencil: mdiPencil,
      mdiPalette: mdiPalette,
      mdiRedo: mdiRedo,
      mdiDelete: mdiDelete,
      mdiCrosshairs: mdiCrosshairs,
      mdiClose: mdiClose,
      mdiEye: mdiEye,
      mdiCube: mdiCube,
      mdiArrowExpandVertical: mdiArrowExpandVertical,
      mdiHandRight: mdiHandRight,
      mdiMenuUp: mdiMenuUp,
    },

    // v-models
    leftPanelActiveTab: null,
    bottomDrawerActive: false,

    // config file status and params
    config: {
      loaded: false,
      failed: false,
    },

    // cylinders data
    cylinders: {
      selected: [],
      saved: [],
    },

    // cruise (root) parameters
    cruise: {
      params: {
        meta: {},
        data: [],
        name: null,
        nameIndex: null,
        site: null,
        siteIndex: null,
        startDate: null,
        startDateIndex: null,
        endDate: null,
        endDateIndex: null,
        fatesSelected: [],
        dataString: null,
      },
      opts: {
        names: [],
        sites: [],
        dates: [],
        fates: [],
      },
    },

    // map view parameters
    map: {
      flags: {
        viewActive: false, // whether to show the map view or not
      },
      params: {
        dragMode: null,
        dragColor: null,
        dragColorIndex: null,
      },
      opts: {
        backgrounds: [],
        dragColors: {
          Pearl_White: {
            text: "#000000",
            background: "#FFFFFF",
          },
          Crab_Red: {
            text: "#FFFFFF",
            background: "#E32227",
          },
          Ocean_Blue: {
            text: "#FFFFFF",
            background: "#189AB4",
          },
          Seafoam_Green: {
            text: "#000000",
            background: "#93E9BE",
          },
          Microbial_Orange: {
            text: "#FFFFFF",
            background: "#F28500",
          },
          Seafloor_Black: {
            text: "#FFFFFF",
            background: "#000000",
          },
        },
      },
    },

    // core view parameters
    core: {
      flags: {
        attrMenuActive: false, // to show attribute menu
      },
      variables: {
        hasData: false, // whether, after parsing, there's data for the selected vars
        search: "", // search query
        selected: [],
        category: "Geochemistry",
        categoryIndex: 0,
        categories: ["Meta", "Geochemistry", "Taxa"],
        all: {}, // will be populated in `loadCruise`
        allFiltered: [], // filtered list of all variables
      },
      params: {
        attrMenuText: null,
        varBounds: [null, null],
        cmap: null,
        cmapIndex: null,
      },
      opts: {
        cmaps: {
          Viridis: {
            text: "#FFFFFF",
            func: interpolateViridis,
          },
          Cividis: {
            text: "#FFFFFF",
            func: interpolateCividis,
          },
          Greys: {
            text: "#000000",
            func: interpolateGreys,
          },
          Inferno: {
            text: "#FFFFFF",
            func: interpolateInferno,
          },
          Plasma: {
            text: "#FFFFFF",
            func: interpolatePlasma,
          },
          Magma: {
            text: "#FFFFFF",
            func: interpolateMagma,
          },
        },
      },
    },

    // interpolation view parameters
    interp: {
      flags: {
        attrMenuActive: false, // to show attribute menu
        methodMenuActive: false, // to show method menu
        variablesChanged: false, // whether variable was changed by user
        resolutionChanged: false, // whether user changed the resolution
        viewActive: false, // to show the interp view component
        viewLoading: false, // to show loading message
        viewFailed: false, // to show failure message
        viewNonWindowsDetectedDuringInterp: false, // to show message when non-Windows OS detected during interpolation
      },
      variables: {
        hasData: false, // whether, after parsing, there's data for the selected vars
        search: "", // search query
        selected: [],
        category: "Geochemistry",
        categoryIndex: 0,
        categories: ["Meta", "Geochemistry", "Taxa"],
        all: {}, // will be populated in `loadCruise`
        allFiltered: [], // filtered list of all variables
      },
      params: {
        data: [],
        attrMenuText: null,
        method: null,
        methodIndex: null,
        resolution: null,
        colorMode: null,
        colorModeIndex: null,
        colorModeLegend: null,
        colorModeLegendHeight: null,
        cmap: null,
        cmapIndex: null,
        showValues: null,
        shapeType: null,
        geoHeight: null,
        mouseMode: null,
      },
      opts: {
        methods: ["Natural", "Linear"],
        resolutions: [7, 14, 21],
        cmaps: {
          Viridis: {
            text: "#FFFFFF",
            func: interpolateViridis,
          },
          Cividis: {
            text: "#FFFFFF",
            func: interpolateCividis,
          },
          Greys: {
            text: "#000000",
            func: interpolateGreys,
          },
          Inferno: {
            text: "#FFFFFF",
            func: interpolateInferno,
          },
          Plasma: {
            text: "#FFFFFF",
            func: interpolatePlasma,
          },
          Magma: {
            text: "#FFFFFF",
            func: interpolateMagma,
          },
        },
      },
      // mode: "Manual",
      // modes: ["Manual", "File"],
      // file: null,
      // files: {
      //   Pescadero: [
      //     "Pescadero_3d_natural_5cm.csv",
      //     "Pescadero_3d_natural_10cm.csv",
      //     "Pescadero_3d_natural_15cm.csv",
      //     "Pescadero_3d_linear_5cm.csv",
      //     "Pescadero_3d_linear_10cm.csv",
      //     "Pescadero_3d_linear_15cm.csv",
      //   ],
      //   "Santa Monica": [],
      // },
    },
  }),

  computed: {
    fatesSelectAllIcon() {
      let vm = this;
      const allFatesSelected =
        vm.cruise.params.fatesSelected.length === vm.cruise.opts.fates.length;
      const someFatesSelected =
        vm.cruise.params.fatesSelected.length > 0 && !allFatesSelected;
      if (allFatesSelected) {
        return vm.icons.mdiCloseBox;
      } else if (someFatesSelected) {
        return vm.icons.mdiMinusBox;
      } else {
        return vm.icons.mdiCheckboxBlankOutline;
      }
    },

    locationMenuText: function () {
      return `${this.cruise.params.name} → ${this.cruise.params.site}`;
    },

    dateRangeMenuText: function () {
      let vm = this;
      if (vm.cruise.params.startDate && vm.cruise.params.endDate) {
        const startDateStr = vm.getDateFormatted(vm.cruise.params.startDate);
        const endDateStr = vm.getDateFormatted(vm.cruise.params.endDate);
        return `${startDateStr} → ${endDateStr}`;
      } else {
        return "";
      }
    },

    interpMethodMenuText: function () {
      return this.interp.params.method && this.interp.params.resolution
        ? `${this.interp.params.method} → ${this.interp.params.resolution}cm`
        : "";
    },

    coreViewColorModeMenuText: function () {
      if (this.showCoreView && this.core.params.cmap) {
        return `${this.core.params.cmap}`;
      } else {
        return "";
      }
    },

    interpViewColorModeMenuText: function () {
      if (
        this.interp.flags.viewActive &&
        this.interp.params.colorMode &&
        this.interp.params.cmap
      ) {
        return `${this.interp.params.colorMode} → ${this.interp.params.cmap}`;
      } else {
        return "";
      }
    },

    showCoreView: function () {
      return (
        this.cylinders.selected.length > 0 &&
        this.core.variables.selected.length > 0
      );
    },
  },

  mounted: function () {
    let vm = this;

    // set defaults
    vm.cruise.params.nameIndex = 0;
    vm.cruise.params.siteIndex = 0;
    vm.cruise.params.site = "All Sites";

    vm.map.params.dragMode = "Zoom";
    vm.map.params.dragColorIndex = 0;
    vm.map.params.dragColor = Object.keys(vm.map.opts.dragColors)[
      vm.map.params.dragColorIndex
    ];

    vm.core.params.attrMenuText = "";
    vm.core.params.cmapIndex = 0;
    vm.core.params.cmap = Object.keys(vm.core.opts.cmaps)[
      vm.core.params.cmapIndex
    ];

    vm.interp.params.attrMenuText = "";
    vm.interp.params.methodIndex = 0;
    vm.interp.params.method =
      vm.interp.opts.methods[vm.interp.params.methodIndex];
    vm.interp.params.colorModeIndex = 0;
    vm.interp.params.colorMode = "Standard";
    vm.interp.params.colorModeLegendHeight = 0;
    vm.interp.params.cmapIndex = 0;
    vm.interp.params.cmap = Object.keys(vm.interp.opts.cmaps)[
      vm.interp.params.cmapIndex
    ];
    vm.interp.params.showValues = true;
    vm.interp.params.shapeType = "Prism";
    vm.interp.params.geoHeight = 1;
    vm.interp.params.mouseMode = "Orbit";

    // start the show!
    vm.loadConfig(); // load entry-point file to start the program
  },

  watch: {
    "cruise.params.name": function () {
      let vm = this;
      vm.cruise.params.site = "All Sites"; // reset to All Sites
      vm.cruise.params.siteIndex = 0; // for the site list
      vm.cylinders.selected = []; // remove selected cylinders
      vm.resetInterpViewFlags(); // reset view flags
      vm.resetInterpParams(); // reset the inputs to the interpolation
      vm.loadCruise(); // load new cruise meta and data
    },

    "core.variables.search": function () {
      this.getCoreViewAttrMenuVariables();
    },

    "interp.variables.search": function () {
      this.getInterpViewAttrMenuVariables();
    },
  },

  methods: {
    handleAxiosError(error) {
      if (error.response) {
        // Request made and server responded
        console.log(error.response.data);
        console.log(error.response.status);
        console.log(error.response.headers);
      } else if (error.request) {
        // The request was made but no response was received
        console.log(error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.log("Error", error.message);
      }
    },

    loadConfig() {
      let vm = this;
      const configURL = `${vm.publicPath}assets/config.json`;
      axios({
        method: "GET",
        url: configURL,
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      })
        .then((res) => {
          vm.cruise.opts.names = res.data.cruises; // get cruise names from config file
          vm.config.loaded = true; // let the main interface load
          vm.cruise.params.name = vm.cruise.opts.names[0]; // load first cruise in list
        })
        .catch((error) => vm.handleAxiosError(error));
    },

    loadCruise() {
      let vm = this;

      // get cruise DATA (CSV)
      const csvURL = `${vm.publicPath}assets/data/${vm.cruise.params.name}.csv`;
      axios({
        method: "GET",
        url: csvURL,
        headers: {
          Accept: "text/csv",
          "Content-Type": "text/csv",
          "Access-Control-Allow-Origin": "*",
        },
      })
        .then((res) => {
          // store text to send to backend for processing
          vm.cruise.params.dataString = res.data;
          // parse csv data, where each row becomes an object
          csv.toObjects(res.data, {}, (err, data) => {
            if (err) {
              console.error(err);
            } else {
              if (data.length > 0) {
                // get sites
                vm.cruise.opts.sites = vm.getCruiseSites(data);
                // get dates
                vm.cruise.opts.dates = vm.getCruiseDates(data);
                const nDates = vm.cruise.opts.dates.length - 1;
                vm.cruise.params.startDateIndex = 0; // set the start date index
                vm.cruise.params.startDate = vm.cruise.opts.dates[0]; // set the start date
                vm.cruise.params.endDateIndex = nDates; // set the end date index
                vm.cruise.params.endDate = vm.cruise.opts.dates[nDates]; // set the end date
                // get fates
                vm.cruise.opts.fates = vm.getCruiseCoreFates(data);
                vm.cruise.params.fatesSelected = vm.cruise.opts.fates; // select all fates to start
                // update MapView component
                vm.cruise.params.data = data; // this should propogate to MapView.vue
                vm.map.flags.viewActive = true; // let the map view load
              } else {
                console.log("no data for the selected cruise.");
                vm.map.flags.viewActive = false; // hide the map view
              }
            }
          });
        })
        .catch((error) => vm.handleAxiosError(error));

      // get cruise META (JSON)
      const jsonURL = `${vm.publicPath}assets/meta/${vm.cruise.params.name}.json`;
      axios({
        method: "GET",
        url: jsonURL,
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      })
        .then((res) => {
          vm.cruise.params.meta = res.data; // store meta data (JSON)
          vm.map.opts.backgrounds = vm.cruise.params.meta.backgrounds; // parse backgrounds from JSON
          vm.map.opts.backgrounds.splice(0, 0, "None"); // insert None option at front
          vm.parseMetaVars(); // parse variables from JSON
        })
        .catch((error) => vm.handleAxiosError(error));
    },

    getCruiseSites(newData) {
      if (newData.length > 0) {
        let siteList = [...new Set(newData.map((p) => p["Location"]))];
        siteList.unshift("All Sites");
        return siteList;
      } else {
        return [];
      }
    },

    getCruiseDates(newData) {
      if (newData.length > 0) {
        let dateStrList = [...new Set(newData.map((p) => p["Date"]))];
        let dateList = dateStrList.map((d) => {
          const dSplit = d.split("-"); // [yyyy, mm, dd]
          return new Date(dSplit[0], dSplit[1], dSplit[2]);
        });
        const sortedDateList = dateList.slice().sort((a, b) => b.date - a.date);
        return sortedDateList;
      } else {
        return [];
      }
    },

    getCruiseCoreFates(newData) {
      if (newData.length > 0) {
        let coreFateList = [...new Set(newData.map((p) => p["Core Fate"]))];
        return coreFateList;
      } else {
        return [];
      }
    },

    parseMetaVars() {
      let vm = this;
      let allVars = {}; // create new variable map
      let views = [vm.core, vm.interp]; // list of views to parse variables for
      for (let i = 0; i < views.length; i++) {
        const view = views[i];
        view.variables.categories.forEach((category) => {
          if (
            Object.prototype.hasOwnProperty.call(
              vm.cruise.params.meta.variables,
              category
            )
          ) {
            // get interpolation variables from meta file by category
            Object.assign(allVars, {
              [category]: vm.cruise.params.meta.variables[category],
            });
          } else {
            // missing key in JSON!! tell user
            console.log(`Error: Missing key in ${vm.cruise.params.name}.json`);
            console.log(`Missing key: ${category}`);
          }
        });
        // re-assign maps to vue objects, allowing them to be reactive
        view.variables.all = Object.assign({}, view.variables.all, allVars);
        // set the filtered list for searching
        view.variables.allFiltered =
          view.variables.all[view.variables.category];
      }
    },

    // loadInterpFile() {
    //   let vm = this;
    //   vm.cylinders.selected = []; // clear any current cylinders selected
    //   vm.resetInterpViewFlags(); // reset view flags
    //   vm.interp.flags.viewLoading = true; // only show loading box
    //   const url = `${vm.publicPath}assets/data/${vm.interp.file}`;
    //   axios({
    //     method: "GET",
    //     url: url,
    //     headers: {
    //       Accept: "text/csv",
    //       "Content-Type": "text/csv",
    //       "Access-Control-Allow-Origin": "*",
    //     },
    //   })
    //     .then((res) => {
    //       // parse csv data, where each row becomes an object
    //       csv.toObjects(res.data, {}, (err, data) => {
    //         if (err) {
    //           console.error(err);
    //         } else {
    //           vm.cylinders.selected = [
    //             ...new Set(data.map((item) => item.Cylinder)),
    //           ]; // get cylinders in the data set
    //           vm.interp.params.resolution = parseInt(
    //             vm.interp.file.split(".")[0].split("_")[3].replace("cm", "")
    //           ); // get resolution from file name
    //           vm.interp.params.data = data; // this should propogate to InterpView.vue
    //           vm.interp.flags.viewActive = true; // show the component
    //           vm.interp.flags.viewLoading = false; // hide loading icon
    //         }
    //       });
    //     })
    //     .catch((error) => {
    //       vm.handleAxiosError(error);
    //       vm.interp.flags.viewFailed = true; // show failure message
    //       vm.interp.flags.viewLoading = false; // hide loading icon
    //     });
    // },

    getInterp() {
      let vm = this;
      if (
        vm.cylinders.selected.length > 0 &&
        vm.interp.variables.selected.length > 0 &&
        vm.interp.params.method &&
        vm.interp.params.resolution
      ) {
        vm.resetInterpViewFlags(); // reset view flags
        const os = vm.getOS(); // get the system running the program
        if (vm.interp.params.method == "Natural" && !os.includes("Windows")) {
          // Natural Neighbors interpolation ONLY works on Windows!!
          vm.interp.flags.viewNonWindowsDetectedDuringInterp = true; // show error when non-Windows OS detected during interpolation
        } else {
          vm.interp.flags.viewLoading = true; // show loading message
          const params = {
            cruise_data_string: vm.cruise.params.dataString, // send raw data string to backend
            method: vm.interp.params.method, // 'Linear' or 'Natural' => interpolation method to use
            resolution: vm.interp.params.resolution, // interval to interpolate, in cm
            color_mode: vm.interp.params.colorMode, // 'Standard' or 'Uncertainty' => calculation parameter
            cylinders: vm.cylinders.selected, // cylindes selected
            variables: vm.interp.variables.selected, // variables selected
            category: vm.interp.variables.category, // category of variable selected
          };
          axios({
            method: "POST",
            url: vm.backendURL + "/getInterp",
            data: params,
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*",
            },
          })
            .then(function (res) {
              vm.interp.params.data = res.data; // this should propogate to InterpView.vue
              if (vm.interp.params.data.length > 0) {
                vm.interp.flags.viewActive = true; // show the component
              } else {
                vm.interp.flags.viewFailed = true; // show failure message
              }
              vm.interp.flags.viewLoading = false; // hide loading icon
            })
            .catch(function (error) {
              vm.handleAxiosError(error);
              vm.interp.flags.viewFailed = true; // show failure message
              vm.interp.flags.viewLoading = false; // hide loading icon
            });
        }
      }
    },

    getOS() {
      let os = "-";
      const clientStrings = [
        { s: "Windows 10", r: /(Windows 10.0|Windows NT 10.0)/ },
        { s: "Windows 8.1", r: /(Windows 8.1|Windows NT 6.3)/ },
        { s: "Windows 8", r: /(Windows 8|Windows NT 6.2)/ },
        { s: "Windows 7", r: /(Windows 7|Windows NT 6.1)/ },
        { s: "Windows Vista", r: /Windows NT 6.0/ },
        { s: "Windows Server 2003", r: /Windows NT 5.2/ },
        { s: "Windows XP", r: /(Windows NT 5.1|Windows XP)/ },
        { s: "Windows 2000", r: /(Windows NT 5.0|Windows 2000)/ },
        { s: "Windows ME", r: /(Win 9x 4.90|Windows ME)/ },
        { s: "Windows 98", r: /(Windows 98|Win98)/ },
        { s: "Windows 95", r: /(Windows 95|Win95|Windows_95)/ },
        {
          s: "Windows NT 4.0",
          r: /(Windows NT 4.0|WinNT4.0|WinNT|Windows NT)/,
        },
        { s: "Windows CE", r: /Windows CE/ },
        { s: "Windows 3.11", r: /Win16/ },
        { s: "Android", r: /Android/ },
        { s: "Open BSD", r: /OpenBSD/ },
        { s: "Sun OS", r: /SunOS/ },
        { s: "Chrome OS", r: /CrOS/ },
        { s: "Linux", r: /(Linux|X11(?!.*CrOS))/ },
        { s: "iOS", r: /(iPhone|iPad|iPod)/ },
        { s: "Mac OS X", r: /Mac OS X/ },
        { s: "Mac OS", r: /(Mac OS|MacPPC|MacIntel|Mac_PowerPC|Macintosh)/ },
        { s: "QNX", r: /QNX/ },
        { s: "UNIX", r: /UNIX/ },
        { s: "BeOS", r: /BeOS/ },
        { s: "OS/2", r: /OS\/2/ },
        {
          s: "Search Bot",
          r: /(nuhk|Googlebot|Yammybot|Openbot|Slurp|MSNBot|Ask Jeeves\/Teoma|ia_archiver)/,
        },
      ];
      for (let id in clientStrings) {
        let cs = clientStrings[id];
        if (cs.r.test(navigator.userAgent)) {
          os = cs.s;
          break;
        }
      }
      return os;
    },

    getCMapLinearGradient(cmap) {
      return `
        linear-gradient(
          90deg, 
          ${cmap(0.0)}, 
          ${cmap(0.1)},
          ${cmap(0.2)},
          ${cmap(0.3)},
          ${cmap(0.4)},
          ${cmap(0.5)},
          ${cmap(0.6)}, 
          ${cmap(0.7)},
          ${cmap(0.8)},
          ${cmap(0.9)},
          ${cmap(1.0)}
        )
      `;
    },

    getSavedCoreDataBinned(data, variable) {
      const valuesPerBin = Math.round(data.length / 10); // aim for 10 bins
      const dataBinned = []; // collection of bin averages
      let currBin = [data[0][`${variable}_prct`]]; // current bin
      for (let i = 1; i < data.length; i++) {
        if (i % valuesPerBin == 0) {
          const avg = currBin.reduce(function (p, c, i) {
            return p + (c - p) / (i + 1); // get bin average
          }, 0);
          dataBinned.push(avg); // save average
          currBin = []; // empty current bin
        }
        currBin.push(data[i][`${variable}_prct`]);
      }
      return dataBinned;
    },

    getSavedCoreLinearGradient(v) {
      if (v == null) {
        return `linear-gradient(
          90deg, 
          transparent 100%
        )`;
      } else {
        return `linear-gradient(
          90deg, 
          #C4C4C4 ${v * 100}%, 
          transparent ${v * 100}%, 
          transparent 100%
        )`;
      }
    },

    getCoreViewAttrMenuVariables: debounce(function () {
      let vm = this;
      const vars = vm.core.variables; // alias
      // update all filtered list
      vars.allFiltered = vars.all[vars.category].filter((item) => {
        return item.toLowerCase().includes(vars.search.toLowerCase());
      });
    }, 500),

    getInterpViewAttrMenuVariables: debounce(function () {
      let vm = this;
      const vars = vm.interp.variables; // alias
      // update all filtered list
      vars.allFiltered = vars.all[vars.category].filter((item) => {
        return item.toLowerCase().includes(vars.search.toLowerCase());
      });
    }, 500),

    getDateFormatted(d) {
      const convert = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
      };
      const dt = d.getDate();
      const mt = d.getMonth() + 1;
      const yr = d.getFullYear();
      return `${dt}-${convert[mt]}-${yr}`;
    },

    resetMapView() {
      let vm = this;
      // reset map to default view
      if (vm.cruise.params.data.length > 0) {
        const nDates = vm.cruise.opts.dates.length - 1;
        vm.cruise.params.startDateIndex = 0; // set the start date index
        vm.cruise.params.startDate = vm.cruise.opts.dates[0]; // set the start date
        vm.cruise.params.endDateIndex = nDates; // set the end date index
        vm.cruise.params.endDate = vm.cruise.opts.dates[nDates]; // set the end date
        vm.cruise.params.fatesSelected = vm.cruise.opts.fates; // select all fates to start
      }
      vm.cruise.params.site = "All Sites";
      vm.cruise.params.siteIndex = 0;
      vm.$refs.mapView.resetView();
    },

    resetInterpViewFlags() {
      let vm = this;
      // hide all of the possible interp view boxes
      vm.interp.flags.viewActive = false;
      vm.interp.flags.viewLoading = false;
      vm.interp.flags.viewFailed = false;
      vm.interp.flags.viewNonWindowsDetectedDuringInterp = false;
    },

    resetInterpParams() {
      let vm = this;
      // set all params to default values
      vm.interp.variables.selected = [];
      vm.interp.params.attrMenuText = "";
      vm.interp.file = null;
      vm.interp.params.method = "Natural";
      vm.interp.params.methodIndex = 0;
      vm.interp.params.resolution = null;
      vm.interp.params.mouseMode = "Orbit";
    },

    resetCoreViewChangedFlags() {
      this.core.flags.variablesChanged = false;
    },

    resetInterpViewChangedFlags() {
      this.interp.flags.variablesChanged = false;
      this.interp.flags.resolutionChanged = false;
    },

    toggleFatesSelectAll() {
      let vm = this;
      const allFatesSelected =
        vm.cruise.params.fatesSelected.length === vm.cruise.opts.fates.length;
      vm.$nextTick(() => {
        if (allFatesSelected) {
          vm.cruise.params.fatesSelected = [];
        } else {
          vm.cruise.params.fatesSelected = vm.cruise.opts.fates.slice();
        }
      });
    },

    toggleShapeType() {
      let vm = this;
      vm.interp.params.shapeType =
        vm.interp.params.shapeType == "Prism" ? "Cylinder" : "Prism";
      vm.setGeoHeight(false); // don't toggle height
    },

    setCoreViewVariableCategory(newCategory) {
      let vm = this;
      if (vm.core.variables.category !== newCategory) {
        vm.core.flags.attrMenuActive = false; // close the menu
        vm.core.variables.category = newCategory; // update category
        vm.core.variables.search = ""; // reset search term
        vm.core.variables.allFiltered = vm.core.variables.all[newCategory]; // reset filtered list
        setTimeout(function () {
          vm.core.flags.attrMenuActive = true; // re-open the menu after 25ms
        }, 25);
      }
    },

    setCoreViewVariable(newVariable) {
      let vm = this;
      if (vm.core.variables.selected[0] !== newVariable) {
        vm.core.flags.attrMenuActive = false; // close the menu
        vm.core.variables.selected = [newVariable]; // updated the selected variable
        vm.core.flags.variablesChanged = true; // set flag for core view to update variable bounds
        vm.core.variables.search = ""; // reset the search query
        vm.core.variables.allFiltered =
          vm.core.variables.all[vm.core.variables.category]; // reset filtered list
        vm.core.params.attrMenuText = `${vm.core.variables.category} → ${vm.core.variables.selected[0]}`; // update menu text
      }
    },

    setInterpViewVariableCategory(newCategory) {
      let vm = this;
      if (vm.interp.variables.category !== newCategory) {
        vm.interp.flags.attrMenuActive = false; // close the menu
        vm.interp.variables.category = newCategory; // update category
        vm.interp.variables.search = ""; // reset search term
        vm.interp.variables.allFiltered = vm.interp.variables.all[newCategory]; // reset filtered list
        setTimeout(function () {
          vm.interp.flags.attrMenuActive = true; // re-open the menu after 25ms
        }, 25);
      }
    },

    setInterpViewVariable(newVariable) {
      let vm = this;
      if (vm.interp.variables.selected[0] !== newVariable) {
        vm.interp.flags.attrMenuActive = false; // close the menu
        vm.interp.variables.selected = [newVariable]; // updated the selected variable
        vm.interp.flags.variablesChanged = true; // set flag for interp view to update variable bounds
        vm.interp.variables.search = ""; // reset the search query
        vm.interp.variables.allFiltered =
          vm.interp.variables.all[vm.interp.variables.category]; // reset filtered list
        vm.interp.params.attrMenuText = `${vm.interp.variables.category} → ${vm.interp.variables.selected[0]}`; // update menu text
        vm.getInterp();
      }
    },

    setInterpMethod(newMethod) {
      let vm = this;
      if (vm.interp.params.method !== newMethod) {
        vm.interp.params.method = newMethod; // update method
        vm.interp.params.resolution = null; // reset resolution, have to select it to close the menu
      }
    },

    setInterpResolution(newResolution) {
      let vm = this;
      if (vm.interp.params.resolution !== newResolution) {
        vm.interp.flags.methodMenuActive = false; // close the menu
        vm.interp.params.resolution = newResolution; // update resolution
        vm.interp.flags.resolutionChanged = true; // set flag to update resolution in interp view
        vm.setGeoHeight(false); // don't toggle height
        vm.getInterp();
      }
    },

    setInterpColorMode(newColorMode) {
      let vm = this;
      if (vm.interp.params.colorMode !== newColorMode) {
        vm.interp.params.colorMode = newColorMode; // update color mode
        vm.getInterp();
      }
    },

    setGeoHeight(toggle) {
      let vm = this;
      // when shape changes, need to recompute shape size and height
      let shapeSize;
      switch (vm.interp.params.shapeType) {
        case "Cylinder":
          shapeSize = 7; // 7 cm diameter
          break;
        case "Prism":
          shapeSize = vm.interp.params.resolution; // based on resolution
          break;
      }
      if (toggle) {
        vm.interp.params.geoHeight =
          vm.interp.params.geoHeight > 1 ? 1 : shapeSize;
      } else {
        if (vm.interp.params.geoHeight > 1)
          vm.interp.params.geoHeight = shapeSize;
      }
    },

    updateDragMode(newDragMode) {
      this.map.params.dragMode = newDragMode;
    },

    updateSelectedCylinders(newSelectedCylinders) {
      let vm = this;
      vm.cylinders.selected = newSelectedCylinders; // update cylinder list
      vm.resetInterpViewFlags(); // reset view flags
      vm.resetInterpParams(); // reset the inputs to the interpolation
    },

    updateShowValues(newShowValues) {
      this.interp.params.showValues = newShowValues;
    },

    updateGeoHeight(newGeoHeight) {
      this.interp.params.geoHeight = newGeoHeight;
    },

    updateInterpMouseMode(newMouseMode) {
      this.interp.params.mouseMode = newMouseMode;
    },

    updateSavedSamples(newSavedSamples) {
      let vm = this;
      const data = newSavedSamples.data;
      const bounds = newSavedSamples.bounds;
      vm.cylinders.saved.push({
        cruise: vm.cruise.params.name,
        site: vm.cruise.params.site,
        latitude: data[0].Latitude_calc,
        longitude: data[0].Longitude_calc,
        variable: vm.interp.variables.selected[0],
        bounds: bounds,
        method: vm.interp.params.method,
        resolution: vm.interp.params.resolution,
        startDepth: data[0].Z,
        finalDepth: data[data.length - 1].Z,
        data: data,
      });
      vm.bottomDrawerActive = true; // open the bottom drawer to see new saved sample
    },

    updateCoreVarHasData(varHasData) {
      this.core.variables.hasData = varHasData;
    },

    updateInterpVarHasData(varHasData) {
      this.interp.variables.hasData = varHasData;
    },

    updateColorModeLegend(newColorModeLegend) {
      let vm = this;
      const svg = select("#color-mode-legend");
      svg.select("g").remove(); // remove previous legend, if possible
      if (newColorModeLegend.legend !== null) {
        svg.append("g").call(newColorModeLegend.legend);
      }
      vm.interp.params.colorModeLegend = newColorModeLegend.legend;
      vm.interp.params.colorModeLegendHeight = newColorModeLegend.height;
    },

    updateCoreVarBounds(varBounds) {
      this.core.params.varBounds = varBounds;
    },

    exportSavedSamples() {
      function pad(num) {
        return num >= 0 && num < 10 ? "0" + num : num + "";
      }
      let vm = this;
      const data = JSON.stringify(vm.cylinders.saved);
      const blob = new Blob([data], { type: "text/plain" });
      const e = document.createEvent("MouseEvents");
      const a = document.createElement("a");
      const d = new Date();
      const yr = d.getFullYear();
      const mt = d.getMonth() + 1; // Months are zero based
      const dt = d.getDate();
      const hr = d.getHours();
      const mn = d.getMinutes();
      const sc = d.getSeconds();
      const ts = `${yr}${pad(mt)}${pad(dt)}T${pad(hr)}${pad(mn)}${pad(sc)}`;
      a.download = `${ts}_saved_samples_${vm.cruise.params.name}.json`;
      a.href = window.URL.createObjectURL(blob);
      a.dataset.downloadurl = ["text/json", a.download, a.href].join(":");
      e.initEvent(
        "click",
        true,
        false,
        window,
        0,
        0,
        0,
        0,
        0,
        false,
        false,
        false,
        false,
        0,
        null
      );
      a.dispatchEvent(e);
    },
  },
};
</script>

<style>
html {
  overflow-y: hidden !important;
}

.v-toolbar__content {
  padding: 0px 8px !important;
}

.custom-tab-item-header {
  background-color: #272727;
}

.custom-tab-item-body {
  height: calc(100vh - 176px);
  background-color: #121212;
}

.location-menu-text-field
  .v-input__control
  .v-input__slot
  .v-text-field__slot
  input,
.date-range-menu-text-field
  .v-input__control
  .v-input__slot
  .v-text-field__slot
  input {
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}

.core-view-color-bar {
  width: 100%;
  height: 50%;
  border-radius: 8px;
}

.core-view-bounds {
  margin: 0;
  width: 100%;
  height: 50%;
}

#color-mode-legend > .legend > g:nth-of-type(2) > path {
  fill: white;
}

#color-mode-legend text {
  font-size: 9px !important;
  fill: white;
}

#color-mode-legend .arc-label line {
  stroke: white;
}

.list-item-rounded,
.list-item-rounded::before {
  border-radius: 4px !important;
}

.ft-sm {
  font-size: 0.7rem;
}

.ft-md {
  font-size: 0.8rem;
}

.ft-lg {
  font-size: 0.9rem;
}

.custom-text-field-input {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.custom-cols-5 {
  width: 14%;
  max-width: 14%;
  flex-basis: 14%;
}

.cylinder-icon {
  fill: #fff;
}

.saved-sample-clear-btn {
  position: absolute !important;
  margin-top: -28px !important;
  margin-right: -28px !important;
  min-width: 24px !important;
  width: 24px !important;
  background-color: #fff !important;
  border-radius: 50% !important;
}

#bottom-drawer {
  z-index: 10;
}

#bottom-drawer-toggle-card {
  position: absolute;
  z-index: 10000;
  width: 50px;
  height: 28px;
  margin-top: -26px;
  background-color: #333;
  border: 2px solid black;
  border-bottom: 2px solid #333;
  border-top-left-radius: 75% !important;
  border-top-right-radius: 75% !important;
  border-bottom-left-radius: 0 !important;
  border-bottom-right-radius: 0 !important;
}

#bottom-drawer-toggle-btn {
  min-width: 100%;
  padding: 0px;
  border-top-left-radius: 75% !important;
  border-top-right-radius: 75% !important;
  border-bottom-left-radius: 0 !important;
  border-bottom-right-radius: 0 !important;
}

#bottom-drawer-toggle-btn::before {
  background-color: transparent !important;
}

#bottom-drawer-content-card {
  overflow-x: auto;
  width: 100%;
  background-color: #333;
  border-top: 2px solid black;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
