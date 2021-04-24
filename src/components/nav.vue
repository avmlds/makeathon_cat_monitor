<template>
    <b-navbar>
        <template #brand>
            <b-navbar-item tag="router-link" :to="{ path: '/' }">
                <p id="logo">ZooMoon</p>
            </b-navbar-item>
        </template>
        <template #start>
            <b-navbar-item tag="router-link" :to="{ path: '/' }">
                Распределение животных
            </b-navbar-item>
            <b-navbar-item tag="router-link" :to="{ path: '/statistic'}">
                Статистика
            </b-navbar-item>
            <b-navbar-dropdown label="Доп. информация">
                <b-navbar-item href="#">
                    About
                </b-navbar-item>
                <b-navbar-item href="#">
                    Contact
                </b-navbar-item>
            </b-navbar-dropdown>
        </template>

        <template #end>
            <b-navbar-item tag="div">
                <div class="buttons">
                    <a class="button is-warning">
                        <strong>Sign up</strong>
                    </a>
                    <a class="button is-light">
                        Log in
                    </a>
                </div>
            </b-navbar-item>
        </template>
    </b-navbar>
</template>

<script>
export default {
  data() {
    return {
      isActive: true
    }
  }
};
</script>

<style>
#logo {
  font-weight: 900;
}
</style>
