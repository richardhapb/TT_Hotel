
<template>
  <div class="form-wrapper">
    <h2>Inicio de Sesión</h2>
    <form @submit.prevent="login">
      <div>
        <label>Email</label>
        <input v-model="email" type="email" required />
      </div>
      <div>
        <label>Contraseña</label>
        <input v-model="password" type="password" required />
      </div>
      <button type="submit">Iniciar Sesión</button>
    </form>
    <p v-if="message">{{ message }}</p>
    <p>
      <button @click="sendResetPasswordLink">¿Olvidaste tu contraseña?</button>
    </p>
    <p v-if="resetMessage">{{ resetMessage }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      message: '',
      resetMessage: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch(`${import.meta.env.VITE_APP_API_URL}/customers/login/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: this.email, password: this.password })
        });
        const data = await response.json();
        if (data.success) {
          this.message = 'Inicio de sesión exitoso';
          // set auth cookies refresh_token
          document.cookie = `refresh_token=${data.access_token}; path=/; SameSite=Lax`;
          this.$router.push('/customer/dashboard');
        } else {
          this.message = data.message;
        }
      } catch (error) {
        this.message = 'Ocurrió un error al iniciar sesión.';
        console.log(error);
      }
    },
    async sendResetPasswordLink() {
      if (this.email === '') {
        this.resetMessage = 'Por favor, introduce tu correo electrónico';
        return;
      }
      try {
        const response = await fetch(`${import.meta.env.VITE_APP_API_URL}/customers/password_reset/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: this.email })
        });
        console.log(response);
        const data = await response.json();
        if (data.success) {
          this.resetMessage = 'Se ha enviado un correo con las instrucciones para restablecer la contraseña.';
        } else {
          this.resetMessage = data.error;
        }
      } catch (error) {
        this.resetMessage = 'Ocurrió un error al enviar el correo.';
        console.log(error);
      }
    }
  }
};
</script>

<style scoped>
/* Agrega estilos personalizados */
</style>
