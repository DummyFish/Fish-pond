<template>
  <v-container fluid>
    <v-row>
      <v-col :cols="12">
        <v-card class="ma-6 pa-6 mt-0">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="headline mb-1"
                >About Fish Pond</v-list-item-title
              >
              <v-list-item-subtitle
                >A active defense system to protect your
                network</v-list-item-subtitle
              >
              <v-list-item-subtitle
                >More information could be found in Github
                repository</v-list-item-subtitle
              >
            </v-list-item-content>
          </v-list-item>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn icon :href="repo">
              <v-icon>
                mdi-github
              </v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
        <v-card class="ma-6 pa-6">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="headline mb-1"
                >Instructions</v-list-item-title
              >
              <v-list-item-subtitle
                >For security reason, only one user is supported in Fish Pond.
                There is no user registration.</v-list-item-subtitle
              >
            </v-list-item-content>
          </v-list-item>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  computed: {
    repo() {
      return this.$store.state.gitRepo
    }
  }
}
</script>

<style></style>
