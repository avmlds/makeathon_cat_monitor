<template>
  <div>
    <section>
      <b-tabs position="is-centered" class="block">
        <b-tab-item label="Волонтеры">
          <b-table
            :data="data"
            :paginated="isPaginated"
            :per-page="perPage"
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
              width="40"
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
          </b-table>
        </b-tab-item>
        <b-tab-item label="Животные"></b-tab-item>
        <b-tab-item label="Оргуг"></b-tab-item>
      </b-tabs>
    </section>
  </div>
</template>

<script>
const data = [
  { 'id': 1, 'first_name': 'Abbie', 'last_name': 'Archer', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 2, 'first_name': 'Abbie', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 3, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 4, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 5, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 6, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 7, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 8, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 9, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 10, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 11, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 12, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 13, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 14, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 15, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 16, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 17, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 18, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 19, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 20, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 21, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 22, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 23, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 24, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 25, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 26, 'first_name': 'Jones', 'last_name': 'Smith', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'},
  { 'id': 27, 'first_name': 'Abbie', 'last_name': 'Archer', 'date': '2016-10-15 13:43:27	', 'gender': 'Муж'}
]

export default {
  data() {
    return {
      data,
      isPaginated: true,
      isPaginationSimple: false,
      isPaginationRounded: false,
      paginationPosition: "bottom",
      defaultSortDirection: "asc",
      sortIcon: "arrow-up",
      sortIconSize: "is-small",
      currentPage: 1,
      perPage: 5,
    };
  },
};
</script>

<style scoped>
</style>
