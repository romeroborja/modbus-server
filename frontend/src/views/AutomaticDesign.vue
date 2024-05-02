<template>
  <div
    class="d-flex justify-content-center mt-12"
    v-if="loading"
  >
    <div class="spinner-border" role="status">
      <span class="sr-only">Loading...</span>
    </div>
  </div>
  <div 
    class="container-fluid pb-4" 
    :class="displayNavPill ? 'mt-4' : ''"
    v-else
  >
    <div class="row align-items-center">
      <div>
        <!-- navPill -->
        <nav-pill
          v-if="displayNavPill"
          :options="navPillOptions"
          @selectedOption="setNavPillOption"
        />
      </div>
    </div>
    <div class="row">
      <div class="col-lg-3">
        <!-- navCard -->
        <nav-card
          v-if="displayNavCard"
          :options="navCardOptions"
          @selectedOption="setNavCardOption"
        />
      </div>
      <div :class="displayNavPill && displayNavCard ? 'col-lg-9 mt-lg-0 mt-4' : ''">
        <!-- table -->
        <edition-table          
          :headers="headers"
          :title="tableTitle"
          :records="registers"
          @applyChanges="setData"
          @saveChanges="saveData"
        />
      </div>
    </div>
  </div>
</template>

<script>
import EditionTable from "@/components/tables/EditionTable.vue";
import NavCard from "@/components/cards/NavCard.vue"
import NavPill from "@/components/NavPill.vue"
import { api } from "@/services/httpClient"
import { getLevel } from "@/helpers/data"

export default {
  data() {
    return {
      data: "",
      navPillOption: "",
      navCardOption: "",
      loading: true,
      headers: {
        address: 'Address',
        name: 'Name',
        format: 'Type',
        scale: 'Gain',        
        value: 'Value',
        unit: 'Unit'
      },
    }
  },
  components: {
    NavPill,
    NavCard,
    EditionTable
  },
  methods: {
    /**
     * Realiza una petición GET al backend para actualizar los registros modbus.
     */
    getData() {
      api.get(`/modbus_registers`)
        .then((result) => {
          if (result && result.status == 200) {
            this.data = result.data.modbus_registers
            this.loading = false
          }
        })
        .catch((err) => {
          console.log(err)
        });
    },
    /**
     * Realiza una petición POST al backend con el valor del registro modificado.
     *
     * @param {Object} newRegister registro modbus con su valor modificado.
     */
     setData(registers) {
      api.post("/modbus_registers", registers)
        .then((result) => {
          if (result.status == 201) {
            this.getData()
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    saveData(registers) {
      api.post("/save_modbus_registers", registers)
        .then((result) => {
          if (result.status == 201) {
            console.log('success save');
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    /**
     * Actualiza el valor de la barra superior de navegación (nav-pill).
     *
     * @param {String} option nombre del subgrupo 1 de los registros modbus.
     */
    setNavPillOption(option) {
      this.navPillOption = option

      if (this.displayNavCard) {
        this.navCardOption = this.navCardOptions[0]
      }
    },
    /**
     * Actualiza el valor de la tarjeta de navegación que se encuentra pegada a la tabla.
     *
     * @param {String} option nombre del subgrupo 2 de los registros modbus.
     */
    setNavCardOption(option) {
      this.navCardOption = option
    },
    /**
     * Permite cerrar el mensaje de error flotante que aparece en la interfaz.
     */
    closeError() {
      this.showError = false
    }
  },
 computed: {
    /**
     * Devuelve true si los registros tienen subgrupo 1.
     *
     * @return {Bool}
     */
    displayNavPill() {
      return getLevel(this.data) > 0 ? true : false
    },
    /**
     * Devuelve true si los registros tienen subgrupo 2.
     *
     * @return {Bool}
     */
    displayNavCard() {
      return getLevel(this.data[this.navPillOption]) > 0 ? true : false
    },
    /**
     * Devuelve true si los registros tienen subgrupo 3.
     *
     * @return {Bool}
     */
    displayTableGroups() {
      if (this.navPillOption && this.navCardOption) {
        if (getLevel(this.data[this.navPillOption][this.navCardOption]) > 0) {
          return true
        }
      }
      return false
    },
    /**
     * Devuelve la lista de grupos que forman la barra superior de navegación.
     *
     * @return {Array}
     */
    navPillOptions() {
      return this.displayNavPill ? Object.keys(this.data) : undefined
    },
    /**
     * Devuelve la lista de grupos que forman la tarjeta de navegación.
     *
     * @return {Array}
     */
    navCardOptions() {
      return this.displayNavCard ? Object.keys(this.data[this.navPillOption]) : undefined
    },
    /**
     * Devuelve los registros modbus dependiendo de la selección de los grupos en la interfaz.
     *
     * @return {Object} registros filtrados por grupos.
     */
    registers() {
      if (this.displayNavPill) {
        if (this.displayNavCard) {          
          return this.data[this.navPillOption][this.navCardOption]
        } else {
          return this.data[this.navPillOption]
        }
      } else {
        return this.data
      }
    },
    /**
     * Calcula el nombre a mostrar en la tabla dependiendo de los subgrupos de los registros.
     *
     * @return {String}
     */
    tableTitle() {
      if (this.displayNavPill && this.displayNavCard) {
        return this.navCardOption
      } else if (this.displayNavPill) {
        return this.navPillOption
      } else {
        return this.$route.name
      }
    }
  },
  beforeMount() {
    this.getData()
  },
  mounted() {
    this.interval = setInterval(() => {
      this.getData();
    }, 1000);
  },
  beforeUnmount() {
    clearInterval(this.interval);
  },
};
</script>