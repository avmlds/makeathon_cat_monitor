<template>
  <div>
    <section>
      <b-tabs position="is-centered">
        <b-tab-item label="Список пользователей">
          <b-table
            :bordered="true"
            :data="users"
            @click="checkedRows = []"
            :columns="columns"
            :checked-rows.sync="checkedRows"
            checkable
            :checkbox-position="checkboxPosition"
          >
          </b-table>
          <b-field grouped group-multiline>
            <b-button
              label="Деактивировать выбранных пользователей"
              type="is-danger"
              icon-left="close"
              class="field"
              @click="deactivateUser"
            />
          </b-field>
        </b-tab-item>

        <b-tab-item label="Выбранные пользователи">
          <pre>{{ checkedRows }}</pre>
        </b-tab-item>
      </b-tabs>
    </section>
  </div>
</template>

<script>
import users from "../../users.json";

export default {
  data() {
    return {
      users: users,
      checkboxPosition: "left",
      checkedRows: [],
      columns: [
        {
          field: "user_name",
          label: "Имя пользователя",
          centered: true,
        },
        {
          field: "first_name",
          label: "ФИО",
          centered: true,
        },
      ],
    };
  },
  methods: {
    deactivateUser() {
      for (let i in this.checkedRows) {
        let filteredList = this.users.filter((item) => item.user_name !== this.checkedRows[i].user_name);
        this.users = filteredList;
        }
      }
    }
  }
</script>
