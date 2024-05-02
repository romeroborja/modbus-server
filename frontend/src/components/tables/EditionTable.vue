<template>
    <!--table-->
    <div class="row">
      <div class="col-12">
        <div class="card mt-4 p-4">
          <div class="card-header d-flex justify-content-between">
            <h5 class="mb-0">{{ title }}</h5>
            <div v-if="editable">
              <material-button
                id="apply-changes"
                class="mx-2"
                color="secondary"
                variant="outline"
                size="sm"
                @click="applyChanges"
                :disabled="disableApply"
              >
                Apply changes
              </material-button>              
              <material-button
                id="apply-changes"
                class="mx-2"
                color="secondary"
                variant="outline"
                size="sm"
                @click="saveChanges"
                :disabled="disableSave"
              >
                Save
              </material-button>
            </div>            
          </div>
          <div class="px-0">
            <div class="table-responsive p-0">
              <div
                class="dataTable-wrapper dataTable-loading no-footer sortable fixed-height fixed-columns"
              >
                <!-- Table -->
                <div class="table-container">
                  <table class="table align-items-center mb-0">
                    <thead>
                      <tr>
                        <th
                          v-for="(item, index) in headers"
                          :key="index"
                          class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
                        >
                          {{ item }}
                        </th>
                      </tr>
                    </thead>
                    <template v-if="subgroups">
                      <tbody
                        v-for="(groupRecordss, subgroup) in records"
                        :key="subgroup"
                      >
                        <tr>
                          <th
                            colspan="7"
                            class="text-xl font-weight-bold mb-0 text-center group-row border-top border-bottom"
                          >
                            {{ subgroup }}
                          </th>
                        </tr>
                        <tr v-for="record in groupRecordss" :key="record.address">
                          <template v-if="isReadable(record)">
                            <td
                              v-for="(item, index) in headers"
                              :key="index"
                              class="text-sm font-weight-normal mb-0 align-text"
                            >
                              <template v-if="isWritable(index)">
                                <material-choices
                                  v-if="isCombobox(record)"
                                  :id="record.name"
                                  :ref="`#combobox-${record.name}`"
                                  :class="`input-${inputState(record)}`"
                                  :options="record.enumfield"
                                  :defaultOption="parseInt(record.value)"
                                  @selectedOption="(value) => editRecord(record, value)"
                                />
                                <material-input
                                  v-else
                                  :id="`record-${record.name}`"
                                  :name="`record-${record.name}`"
                                  :class="`input-${inputState(record)}`"
                                  :key="record.name"
                                  type="text"
                                  size="md"
                                  variant="static"
                                  :modelValue="currentValue(record)"
                                  @input="editRecord(record, $event.target.value)"
                                />
                              </template>
                              <template v-else>
                                {{ record[index] }}
                              </template>
                            </td>
                          </template>
                        </tr>
                      </tbody>
                    </template>
                    <template v-else>
                      <tbody>
                        <tr v-for="record in records" :key="record.address">
                          <template v-if="isReadable(record)">
                            <td
                              v-for="(item, index) in headers"
                              :key="index"
                              class="text-sm font-weight-normal mb-0 align-text"
                            >
                              <template v-if="isWritable(index)">
                                <material-choices
                                  v-if="isCombobox(record)"
                                  :id="record.name"
                                  :ref="`#combobox-${record.name}`"
                                  :class="`input-${inputState(record)}`"
                                  :options="record.enumfield"
                                  :defaultOption="parseInt(record.value)"
                                  @selectedOption="(value) => editRecord(record, value)"
                                />
                                <material-input
                                  v-else
                                  :id="`record-${record.name}`"
                                  :name="`record-${record.name}`"
                                  :class="`input-${inputState(record)}`"
                                  :key="record.name"
                                  type="text"
                                  size="md"
                                  variant="static"
                                  :modelValue="currentValue(record)"
                                  @input="editRecord(record, $event.target.value)"
                                />
                              </template>
                              <template v-else>
                                {{ record[index] }}
                              </template>
                            </td>
                          </template>
                        </tr>
                      </tbody>
                    </template>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import MaterialInput from "@/components/MaterialInput.vue"
  import MaterialChoices from "@/components/MaterialChoices.vue"
  import MaterialButton from "@/components/MaterialButton.vue"
  
  export default {
    name: "edition-table",
    components: {
      MaterialInput,
      MaterialButton,
      MaterialChoices
    },
    props: {
      title: {
        type: String,
        default: "",
      },
      headers: {
        type: Object,
      },
      records: {
        type: Object,
      },
      editable: {
        type: Boolean,
        default: true,
      },
      subgroups: {
        type: Boolean,
        default: false,
      },
    },
    emits: ["applyChanges","saveChanges"],
    data() {
      return {
        recordsModified: {},
        recordsError: {},
      };
    },
    computed: {
      // Habilitar el botón de aplicar cambios solo cuando haya algún registro modificado
      disableApply() {
        return !(Object.keys(this.recordsModified).length > 0);
      },
      disableSave() {
        return !this.disableApply
      }
    },
    methods: {
      inputState(record) {
        // Muestra el valor del registro resaltado para que el cliente vea que se ha modificado
        return Object.prototype.hasOwnProperty.call(
          this.recordsModified,
          record["name"]
        )
          ? "modified"
          : Object.prototype.hasOwnProperty.call(
              this.recordsError,
              record["name"]
            )
          ? "error"
          : "";
      },
      isReadable(record) {
        if (record.permissions) {
          if (!record.permissions.includes("R")) return false          
        }
        return true
      },
      isWritable(colName) {
        if (colName !== "value") return false
        return true
      },
      editRecord(record, inputValue) {
        if (inputValue != record["value"]) {
          if (
            record["min"] &&
            record["max"] &&
            (inputValue < record["min"] || inputValue > record["max"])
          ) {
            this.recordsError[record["name"]] = {
              data: record,
              new_value: inputValue,
            };
            delete this.recordsModified[record["name"]];
          } else {
            this.recordsModified[record["name"]] = {
              data: record,
              new_value: inputValue,
            };
            delete this.recordsError[record["name"]];
          }
        } else {
          delete this.recordsModified[record["name"]];
          delete this.recordsError[record["name"]];
        }
      },
      // Remplaza el valor original por el modificado por el cliente
      currentValue(record) {
        if (this.recordsModified[record["name"]]) {
          return this.recordsModified[record["name"]].new_value;
        } else if (this.recordsError[record["name"]]) {
          return this.recordsError[record["name"]].new_value;
        } else {
          return record["value"];
        }
      },
      applyChanges() {
        this.$emit("applyChanges", this.recordsModified);
        this.recordsModified = {};
      },
      isCombobox(record) {
        return record.enumfield
      },
      saveChanges() {
        this.$emit("saveChanges", this.records);        
      }
    },
  };
  </script>
  
  <style scope>
  .align-text {
    padding: 0.5rem 1.5rem !important;
  }
  tr:nth-child(even) {
    background-color: #f2f2f2;
  }
  .input-modified {
    background-color: antiquewhite !important;
  }
  .input-error {
    background-color: #fb000069 !important;
  }
  </style>
  