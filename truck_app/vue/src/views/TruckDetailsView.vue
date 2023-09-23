<template>
  <div>
    <div class="truck-details backdrop">
      <HeaderComponent />
      <div class="main">
        <div v-if="truck" class="content-div">
          <div class="licence-plate-bg">
            <div
              v-for="(char, index) in splitChars"
              :key="index"
              class="custom-font"
            >
              {{ char }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import HeaderComponent from "../components/HeaderComponent.vue";
export default {
  name: "TruckdetailsView",
  components: {
    HeaderComponent,
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

<style>
.licence-plate-bg {
  background: url("@/assets/Wisconsin licence plate template.png") no-repeat
    center center;
  background-size: cover;
  padding-top: 17px;
  padding-left: 2px;
  padding-right: 2px;
  width: 230px;
  height: 100px;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 3.4em;
  text-shadow: -2px -2px 0 #aaa, 2px -2px 0 #aaa, -2px 2px 0 #aaa,
    2px 2px 0 #aaa;
  display: flex;
  justify-content: center;
  align-items: center;
}
.custom-font {
  font-family: "Modulario", sans-serif;
  transform: scaleX(0.5);
  letter-spacing: -10px;
}
.content-div {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
