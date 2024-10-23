
<template>
    <div class="form-wrapper">
      <h1>Verificación  de Correo Electrónico</h1>
      <h2>Crea tu contraseña</h2>
      <form @submit.prevent="createPassword">
        <div>
          <label>Nueva Contraseña</label>
          <input v-model="password" type="password" required />
        </div>
        <div>
          <label>Confirmar Contraseña</label>
          <input v-model="passwordConfirm" type="password" required />
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
        passwordConfirm: '',
        password: '',
        token: '',
        message: '',
        email: ''
      };
    },
    mounted() {
      this.token = this.$route.params.token;
      this.verifyEmail(this.token); 
    },
    methods: {
      async verifyEmail(token) {
        try {
          const response = await fetch(`${import.meta.env.VITE_APP_API_URL}/email/verify/${token}`);
          const data = await response.json();
          if (data.success) {
            this.message = 'Verificación exitosa. Crea tu contraseña.';
            this.email = data.email;
            return data;
          } else {
            this.message = data.error;
            return data;
          }
        } catch (error) {
          this.message = 'Error al verificar. Intenta nuevamente.';
          console.log(error);
        }
        
      },
      async createPassword() {
        try {

          if (this.password !== this.passwordConfirm) {
            this.message = 'Las contraseñas no coinciden';
            return;
          }
          const response = await fetch(`${import.meta.env.VITE_APP_API_URL}/customers/set_password/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              email: this.email,
              password: this.password })
          });
          console.log(response)
          const data = await response.json();

          if (data.success) {
            this.message = 'Contraseña creada correctamente';
            this.$router.push('/customer/dashboard');
          } else {
            alert(data.error + ". Te redirigimos a la página de inicio de sesión. Selecciona ¿Olvidaste tu contraseña? para restablecerla.");
            this.$router.push('/login');
          }
        } catch (error) {
          alert('Ocurrió un error al cambiar la contraseña. Te redirigimos a la página de inicio. Selecciona ¿Olvidaste tu contraseña? para restablecerla.');
          this.$router.push('/login');
          console.log(error);
        }
      }
    }
  };
  </script>
