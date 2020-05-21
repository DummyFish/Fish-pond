<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" align="center">
        <v-card class="ma-6 pa-6" height="50%" width="50%">
          <v-cart-text class="display-1 text--primary">
            Reset Password
          </v-cart-text>
          <v-card-actions>
            <v-text-field
              v-model="password"
              :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="[rules.required, rules.min]"
              :type="show1 ? 'text' : 'password'"
              name="password"
              label="New Password"
              hint="At least 8 characters"
              counter
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
              @click:append="show2 = !show2"
            ></v-text-field>
          </v-card-actions>
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
      }
    }
  }
}
</script>

<style></style>
