<template>
  <v-app dark>
    <v-navigation-drawer app permanent>
      <v-list>
        <v-list-item link>
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
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-rocket</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Dashboard</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-toolbox</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Services</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-account-cog</v-icon>
          </v-list-item-icon>
          <v-list-item-title>User setting</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-content>
      <nuxt />
    </v-content>
  </v-app>
</template>

<script>
export default {}
</script>
