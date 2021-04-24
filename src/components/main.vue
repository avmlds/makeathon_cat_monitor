<template>
  <div class="container">
    <p id="cr">Карта распределения животных</p>
    <br>
    <gmap-map v-bind="options" id="map">
      <gmap-info-window
        :options="infoOptions"
        :position="infoPosition"
        :opened="infoOpened"
        @closeclick="infoOpened = false"
      >
        {{ infoContent }}
      </gmap-info-window>

      <gmap-marker
        v-for="(item, key) in coordinates"
        :key="key"
        :icon="{ url: require('../assets/pets.png')}"
        :position="getPosition(item)"
        :clickable="true"
        @click="toggleInfo(item, key)"
      />
    </gmap-map>
  </div>
</template>

<script>
import { gmapApi } from "vue2-google-maps";

export default {
  data() {
    return {
      options: {
        zoom: 12,
        center: {
          lat: 55.748716,
          lng: 37.612828,
        },
        mapTypeId: "terrain",
      },
      coordinates: {
        0: {
          full_name: "Мертвый петух",
          lat: "55.748716",
          lng: "37.612828",
        },
        1: {
          full_name: "Гнусавый пёс",
          lat: "55.748916",
          lng: "37.762928",
        },
      },
      infoPosition: null,
      infoContent: null,
      infoOpened: false,
      infoCurrentKey: null,
      infoOptions: {
        pixelOffset: {
          width: 0,
          height: -35,
        },
      },
    };
  },
  computed: {
    google: gmapApi,
  },
  methods: {
    getPosition: function (marker) {
      return {
        lat: parseFloat(marker.lat),
        lng: parseFloat(marker.lng),
      };
    },
    toggleInfo: function (marker, key) {
      this.infoPosition = this.getPosition(marker);
      this.infoContent = marker.full_name;
      if (this.infoCurrentKey == key) {
        this.infoOpened = !this.infoOpened;
      } else {
        this.infoOpened = true;
        this.infoCurrentKey = key;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
#map {
  height: 500px;
  width: 100%;
  margin: 0 auto;
}
</style>
