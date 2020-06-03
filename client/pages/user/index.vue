<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" align="center">
        <v-card class="ma-6 pa-6" height="50%" width="50%">
          <v-card-text class="display-1 text--primary">
            Reset Password
          </v-card-text>
          <v-form v-model="isValid">
            <v-card-actions class="d-flex flex-column align-stretch">
              <v-text-field
                v-model="password"
                :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[rules.required, rules.min]"
                :type="show1 ? 'text' : 'password'"
                name="password"
                label="New Password"
                hint="At least 8 characters"
                counter
                width="100%"
                @click:append="show1 = !show1"
              ></v-text-field>
              <v-spacer></v-spacer>
              <v-text-field
                :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[rules.required, rules.match]"
                :type="show2 ? 'text' : 'password'"
                name="confirm password"
                label="Confirm Password"
                hint="At least 8 characters"
                width="100%"
                @click:append="show2 = !show2"
              ></v-text-field>
              <v-spacer></v-spacer>
              <v-btn
                text
                class="ma-5"
                :disabled="!isValid"
                @click="userLogin(password)"
                >Submit</v-btn
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
  data() {
    return {
      show1: false,
      show2: false,
      password: '',
      rules: {
        required: (value) => !!value || 'Required.',
        min: (value) => value.length >= 8 || 'Min 8 characters',
        match: (value) =>
          this.password === value || "The password you entered doesn't match"
      },
      isValid: false
    }
  },
  methods: {
    async userLogin(password) {
      try {
        // const response =
        await this.$axios.patch('/api/auth/reset_password', {
          data: password
        })
        this.logout()
        // this.$auth.setToken('local', 'Bearer ' + response.data.token)
        // console.log(response)
      } catch (err) {
        console.log(err)
      }
    },
    async logout() {
      const response = await this.$auth.logout()
      console.log(response)
    }
  }
}
</script>

<style></style>
