import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

import CylinderIcon from "@/models/Icons/CylinderIcon.vue";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    dark: true,
    options: { customProperties: true },
  },
  icons: {
    iconfont: "mdiSvg",
    values: {
      cylinder: {
        component: CylinderIcon,
      },
    },
  },
});
