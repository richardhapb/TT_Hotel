
<template>
  <div class="wrapper">
    <h1>Sorteo de San Valentín</h1>
    <p>¡Ven a disfrutar de nuestro hotel!</p>
      <p>Registrate y participa en el sorteo de San Valentín con 2 noches tú y tu pareja con todo pagado en el hotel</p>
  </div>
  <div class="form-wrapper">
    <h2>Crear Cuenta</h2>
    <form @submit.prevent="register">
      <div>
        <label>Email</label>
        <input v-model="email" type="email" required />
      </div>
      <div>
        <label>Nombre</label>
        <input v-model="name" type="text" required />
      </div>
      <div>
        <label>Teléfono</label>
        <input v-model="phone" type="tel" required />
        <small>Solo números (Ej: 923456789)</small>
      </div>
      <button type="submit">Registrarse</button>
    </form>
    <p v-if="message">{{ message }}</p>
    <p>
      ¿Ya tienes una cuenta? <router-link to="/login">Inicia sesión</router-link>
    </p>
  </div>
  <div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      name: '',
      phone: '',
      message: ''
    };
  },
  methods: {
    async register() {
      try {
        if (this.email === '') {
          this.message = 'Por favor, introduce tu correo electrónico';
          return;
        }
        if (this.name === '') {
          this.message = 'Por favor, introduce tu nombre';
          return;
        }
        if (!/^\d{9}$/.test(this.phone)) {
          this.message = 'Por favor, introduce un número de teléfono válido';
          return;
        }
        const response = await fetch(`${import.meta.env.VITE_APP_API_URL}/customers/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: this.email,
            name: this.name,
            phone: this.phone,
          })
        });
        console.log(response)
        const data = await response.json();
        if (data.success) {
          this.message = 'Registro exitoso. Verifica tu correo electrónico.';
          // Limpiar formulario
          this.email = '';
          this.name = '';
          this.phone = '';
        } else {
          this.message = data.error;
        }
      } catch (error) {
        this.message = 'Error al registrar. Intenta nuevamente.';
        console.log(error);
      }
    }
  }
};
</script>
