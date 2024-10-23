
<template>
    <div class="customer-login">
      <h2>Confirma tu contraseña</h2>
      <form @submit.prevent="confirmPassword">
        <div>
          <label>Contraseña</label>
          <input v-model="password" type="password" required />
        </div>
        <div>
          <label>Confirmar contraseña</label>
          <input v-model="confirmPassword" type="password" required />
        </div>
        <button type="submit">Confirmar</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        password: '',
        confirmPassword: '',
        message: ''
      };
    },
    methods: {
      async confirmPassword() {
        try {
          const response = await fetch('/api/customers/change_password/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: this.password, new_password: this.confirmPassword })
          });
          const data = await response.json();
          if (data.success) {
            this.message = 'Contraseña cambiada correctamente';
            // Redirigir a la página correspondiente
            this.$router.push('/customer/dashboard');
          } else {
            this.message = data.message;
          }
        } catch (error) {
          this.message = 'Ocurrió un error al cambiar la contraseña.';
          console.log(error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* Agrega estilos personalizados */
  </style>