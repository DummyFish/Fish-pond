<template>
  <v-app dark>
    <!-- <v-system-bar> </v-system-bar> -->
    <v-navigation-drawer app clipped permanent>
      <v-list>
        <v-list-item>
          <v-list-item-icon>
            <v-icon large>mdi-fishbowl</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="title">Fish Pond</v-list-item-title>
            <v-list-item-subtitle>A honeypot</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list nav dense>
        <v-list-item link to="/" nuxt>
          <v-list-item-icon>
            <v-icon>mdi-rocket</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Dashboard</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/services" nuxt>
          <v-list-item-icon>
            <v-icon>mdi-toolbox</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Services</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/user" nuxt>
          <v-list-item-icon>
            <v-icon>mdi-account-cog</v-icon>
          </v-list-item-icon>
          <v-list-item-title>User setting</v-list-item-title>
        </v-list-item>
        <v-list-item link to="/about" nuxt>
          <v-list-item-icon>
            <v-icon>mdi-information</v-icon>
          </v-list-item-icon>
          <v-list-item-title>About</v-list-item-title>
        </v-list-item>
        <v-list-item v-if="loggedIn" link @click="logout">
          <v-list-item-icon>
            <v-icon>mdi-logout</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>

        <v-list-item link :href="repo">
          <v-list-item-icon>
            <v-icon>
              mdi-github
            </v-icon>
          </v-list-item-icon>
          <v-list-item-title>Github</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-content>
      <nuxt />
    </v-content>
  </v-app>
</template>

<script>
export default {
  computed: {
    repo() {
      return this.$store.state.gitRepo
    },
    loggedIn() {
      return this.$auth.loggedIn
    }
  },
  methods: {
    async logout() {
      const response = await this.$auth.logout()
      console.log(response)
    }
  }
}
</script>
