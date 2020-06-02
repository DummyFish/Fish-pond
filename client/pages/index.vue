<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" align="center">
        <v-card class="ma-6 pa-6" height="50%" width="50%">
          <v-snackbar v-model="showSnackbar" top>
            Login Failed, Please try again.
            <v-btn color="error" text @click="showSnackbar = false">
              Dismiss
            </v-btn>
          </v-snackbar>
          <v-card-text class="display-1 text--primary">
            Fish Pond Login
          </v-card-text>
          <v-form v-model="isValid">
            <v-card-actions>
              <v-text-field
                v-model="psword"
                :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[rules.required]"
                :type="show ? 'text' : 'password'"
                name="password"
                label="Please enter your password"
                hint="Please enter your password"
                @click:append="show = !show"
                @keydown.enter.native.stop="userLogin(psword)"
              ></v-text-field>
              <v-btn
                text
                class="ma-5"
                :disabled="!isValid"
                @click="userLogin(psword)"
                >Login</v-btn
              >
            </v-card-actions>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    show: false,
    psword: '',
    rules: {
      required: (value) => !!value || 'Required.'
    },
    isValid: false,
    showSnackbar: false
  }),
  methods: {
    async userLogin(psword) {
      try {
        // const response =
        await this.$auth.loginWith('local', {
          data: {
            username: 'default',
            password: psword
          }
        })
        // this.$auth.setToken('local', 'Bearer ' + response.data.token)
        // console.log(response)
        // console.log(this.$auth.loggedIn)
        this.$store.dispatch('fetch_init_data')
        this.$router.push({
          path: '/dashboard'
        })
      } catch (err) {
        // console.log(err)
        this.showSnackbar = true
      }
    }
  }
}
</script>

<style></style>
