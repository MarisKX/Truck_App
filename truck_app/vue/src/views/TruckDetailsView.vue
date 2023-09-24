<template>
  <div>
    <div class="truck-details backdrop">
      <HeaderComponent />
      <div class="main">
        <div v-if="truck" class="content-div">
          <LicencePlateVisualization :splitChars="splitChars" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import HeaderComponent from "../components/HeaderComponent.vue";
import LicencePlateVisualization from "@/components/LicencePlateVisualization.vue";
export default {
  name: "TruckdetailsView",
  components: {
    HeaderComponent,
    LicencePlateVisualization,
  },
  props: ["id"],
  mounted() {
    this.fetchData();
  },
  data() {
    return {
      truck: null,
      splitChars: [],
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get(
          "http://dev.maris.com:8090/api/truck/trucks/" + this.id,
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
            },
          }
        );
        if (response.data) {
          this.truck = response.data;
          console.log(this.truck.licence_plate);
        }
      } catch (error) {
        console.error(error);
      }
    },
  },
  watch: {
    truck: {
      handler(newValue) {
        if (newValue && newValue.licence_plate) {
          this.splitChars = newValue.licence_plate.split("");
        }
      },
      immediate: true,
    },
  },
};
</script>

<style></style>
