<template>
  <div>
    <section>
      <b-tabs position="is-centered" class="block">
        <b-tab-item label="Волонтеры">
          <b-table
            :data="data"
            :paginated="isPaginated"
            :per-page="perPage"
            :searchable="searchable"
            :bordered="isBordered"
            :current-page.sync="currentPage"
            :pagination-simple="isPaginationSimple"
            :pagination-position="paginationPosition"
            :default-sort-direction="defaultSortDirection"
            :pagination-rounded="isPaginationRounded"
            :sort-icon="sortIcon"
            :sort-icon-size="sortIconSize"
            default-sort="id"
            aria-next-label="Next page"
            aria-previous-label="Previous page"
            aria-page-label="Page"
            aria-current-label="Current page"
          >
            <b-table-column
              field="id"
              label="ID"
              width="60"
              sortable
              centered
              numeric
              v-slot="props"
            >
              {{ props.row.id }}
            </b-table-column>

            <b-table-column
              field="first_name"
              label="Имя"
              centered
              sortable
              v-slot="props"
            >
              {{ props.row.first_name }}
            </b-table-column>

            <b-table-column
              field="last_name"
              label="Фамилия"
              centered
              sortable
              v-slot="props"
            >
              {{ props.row.last_name }}
            </b-table-column>

            <b-table-column
              field="date"
              label="Дата регистрации"
              sortable
              centered
              v-slot="props"
            >
              <span class="tag is-success">
                {{ new Date(props.row.date).toLocaleDateString() }}
              </span>
            </b-table-column>

            <b-table-column label="Пол" centered v-slot="props">
              <span>
                {{ props.row.gender }}
              </span>
            </b-table-column>
            <b-table-column
              field="stat"
              label="Кол-во зарегистрированных животных"
              centered
              sortable
              v-slot="props"
            >
              {{ props.row.stat + "/" + "250" }}
            </b-table-column>
          </b-table>
        </b-tab-item>
        <b-tab-item label="Животные">
          <section>
            <b-tabs>
              <b-tab-item label="Table">
                <b-table
                  :data="petTracking.main"
                  :columns="petTracking.columns"
                  :selected.sync="selected"
                  focusable
                  @click="selected = null"
                >
                </b-table>
              </b-tab-item>

              <b-tab-item label="Selected">
                <pre>{{ selected }}</pre>
              </b-tab-item>
            </b-tabs>
          </section>
        </b-tab-item>
        <b-tab-item label="Округа">
          <section>
            <b-table :data="data" :paginated="isPaginated" :per-page="perPage">
              <template v-for="column in columns">
                <b-table-column :key="column.id" v-bind="column">
                  <template
                    v-if="column.searchable && !column.numeric"
                    #searchable="props"
                  >
                    <b-input
                      v-model="props.filters[props.column.field]"
                      placeholder="Найти..."
                      icon="magnify"
                      size="is-small"
                    />
                  </template>
                  <template v-slot="props">
                    {{ props.row[column.field] }}
                  </template>
                </b-table-column>
              </template>
            </b-table>
          </section>
        </b-tab-item>
      </b-tabs>
    </section>
  </div>
</template>

<script>
const data = [
  {
    id: 1,
    first_name: "Евгения",
    last_name: "Безрукова",
    date: "2016-10-15 13:43:27	",
    gender: "М",
    stat: 23,
  },
  {
    id: 2,
    first_name: "Максим",
    last_name: "Седов",
    date: "2020-12-10 13:43:27	",
    gender: "М",
    stat: 58,
  },
  {
    id: 3,
    first_name: "Анна",
    last_name: "Покровская",
    date: "2020-11-11 13:43:27	",
    gender: "Ж",
    stat: 109,
  },
  {
    id: 4,
    first_name: "Александр",
    last_name: "Морозов",
    date: "2016-09-07 13:43:27	",
    gender: "М",
    stat: 9,
  },
  {
    id: 5,
    first_name: "Платон",
    last_name: "Быков",
    date: "2020-06-12 13:43:27	",
    gender: "М",
    stat: 145,
  },
  {
    id: 6,
    first_name: "Ева",
    last_name: "Борисова",
    date: "2020-02-25 13:43:27	",
    gender: "Ж",
    stat: 20,
  },
  {
    id: 7,
    first_name: "Кира",
    last_name: "Казакова",
    date: "2020-10-17 13:43:27	",
    gender: "Ж",
    stat: 85,
  },
  {
    id: 8,
    first_name: "София",
    last_name: "Тощан",
    date: "2016-10-19 13:43:27	",
    gender: "Ж",
    stat: 99,
  },
  {
    id: 9,
    first_name: "Артём",
    last_name: "Сторожилов",
    date: "2016-10-25 13:43:27	",
    gender: "М",
    stat: 13,
  },
  {
    id: 10,
    first_name: "Вероника",
    last_name: "Беликова",
    date: "2020-10-04 13:43:27	",
    gender: "Ж",
    stat: 5,
  },
  {
    id: 11,
    first_name: "Дмитрий",
    last_name: "Тихонов",
    date: "2020-10-25 13:43:27	",
    gender: "М",
    stat: 120,
  },
  {
    id: 12,
    first_name: "Полина",
    last_name: "Гагарина",
    date: "2020-06-06 13:43:27	",
    gender: "Ж",
    stat: 6,
  },
  {
    id: 13,
    first_name: "Дарья",
    last_name: "Стрельцова",
    date: "2021-11-25 13:43:27	",
    gender: "Ж",
    stat: 5,
  },
  {
    id: 14,
    first_name: "Владимир",
    last_name: "Гуженко",
    date: "2019-01-02 13:43:27	",
    gender: "М",
    stat: 3,
  },
  {
    id: 15,
    first_name: "Дарья",
    last_name: "Старпович",
    date: "2018-10-15 13:43:27	",
    gender: "Ж",
    stat: 6,
  },
  {
    id: 16,
    first_name: "Ксения",
    last_name: "Гулякова",
    date: "2016-03-04 13:43:27	",
    gender: "Ж",
    stat: 3,
  },
  {
    id: 17,
    first_name: "Арина",
    last_name: "Косыгина",
    date: "2016-11-04 13:43:27	",
    gender: "Ж",
    stat: 18,
  },
  {
    id: 18,
    first_name: "Вероника",
    last_name: "Шевцова",
    date: "2016-06-15 13:43:27	",
    gender: "Ж",
    stat: 55,
  },
  {
    id: 19,
    first_name: "Мария",
    last_name: "Фролова",
    date: "2016-04-15 13:43:27	",
    gender: "Ж",
    stat: 34,
  },
  {
    id: 20,
    first_name: "Евгений",
    last_name: "Сидоров",
    date: "2016-12-15 13:43:27	",
    gender: "М",
    stat: 76,
  },
  {
    id: 21,
    first_name: "Галина",
    last_name: "Скворцова",
    date: "2016-10-15 13:43:27	",
    gender: "Ж",
    stat: 34,
  },
  {
    id: 22,
    first_name: "Антон",
    last_name: "Гаврилов",
    date: "2016-10-15 13:43:27	",
    gender: "М",
    stat: 54,
  },
  {
    id: 23,
    first_name: "Леонид",
    last_name: "Матвеев",
    date: "2021-09-07 13:43:27	",
    gender: "М",
    stat: 15,
  },
  {
    id: 24,
    first_name: "Михаил",
    last_name: "Новиков",
    date: "2021-07-18 13:43:27	",
    gender: "М",
    stat: 27,
  },
  {
    id: 25,
    first_name: "Дарья",
    last_name: "Шульгина",
    date: "2021-05-03 13:43:27	",
    gender: "Ж",
    stat: 87,
  },
  {
    id: 26,
    first_name: "Алла",
    last_name: "Комарова",
    date: "2021-04-15 13:43:27	",
    gender: "Ж",
    stat: 45,
  },
  {
    id: 27,
    first_name: "Александр",
    last_name: "Косыгин",
    date: "2021-03-02 13:43:27	",
    gender: "М",
    stat: 22,
  },
];

import petTracking from "../../pet_tracking.json";

export default {
  data() {
    return {
      petTracking: petTracking,
      selected: petTracking[1],
      data,
      isPaginated: true,
      isPaginationSimple: false,
      isPaginationRounded: false,
      isBordered: false,
      paginationPosition: "bottom",
      defaultSortDirection: "asc",
      searchable: true,
      sortIcon: "arrow-up",
      sortIconSize: "is-small",
      currentPage: 1,
      perPage: 5,
      columns: [
        {
          field: "first_name",
          label: "Имя",
          searchable: true,
          centered: true,
        },
        {
          field: "last_name",
          label: "Фамилия",
          searchable: true,
          centered: true,
        },
        {
          field: "date",
          label: "Дата регистрации",
          searchable: true,
          centered: true,
        },
        {
          field: "gender",
          label: "Пол",
          searchable: true,
          centered: true,
        },
        {
          field: "stat",
          label: "Кол-во зарегистрированных животных",
          centered: true,
        },
      ],
    };
  },
  computed: {
    groupedItems() {
      return this.petTracking.main.reduce((acc, n) => {
        for (const k in n) {
          acc[k] = acc[k] || {};
          acc[k][n[k]] = (acc[k][n[k]] || 0) + 1;
        }
        return acc;
      }, {});
    },
  },
};
</script>

<style lang="scss">
@import "~bulma/sass/utilities/_all";

// Set your colors
$primary: #ee8229;
$primary-light: findLightColor($primary);
$primary-dark: findDarkColor($primary);
$primary-invert: findColorInvert($primary);
$twitter: #4099ff;
$twitter-invert: findColorInvert($twitter);
$success: #6aad79;

// Lists and maps
$custom-colors: null !default;
$custom-shades: null !default;

// Setup $colors to use as bulma classes (e.g. 'is-twitter')
$colors: mergeColorMaps(
  (
    "white": (
      $white,
      $black,
    ),
    "black": (
      $black,
      $white,
    ),
    "light": (
      $light,
      $light-invert,
    ),
    "dark": (
      $dark,
      $dark-invert,
    ),
    "primary": (
      $primary,
      $primary-invert,
      $primary-light,
      $primary-dark,
    ),
    "link": (
      $link,
      $link-invert,
      $link-light,
      $link-dark,
    ),
    "info": (
      $info,
      $info-invert,
      $info-light,
      $info-dark,
    ),
    "success": (
      $success,
      $success-invert,
      $success-light,
      $success-dark,
    ),
    "warning": (
      $warning,
      $warning-invert,
      $warning-light,
      $warning-dark,
    ),
    "danger": (
      $danger,
      $danger-invert,
      $danger-light,
      $danger-dark,
    ),
  ),
  $custom-colors
);

// Links
$link: $primary;
$link-invert: $primary-invert;
$link-focus-border: $primary;

// Import Bulma and Buefy styles
@import "~bulma";
@import "~buefy/src/scss/buefy";
</style>
