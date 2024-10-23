
<template>
  <div class="wrapper">
    <h2>Bienvenido {{ customer.name }}</h2>
    <p>¡Bienvenido a nuestro hotel de San Valentín!</p>
    <p> Ya te encuentras participando en el sorteo de San Valentín.</p>
    <p>¡Disfruta de tus servicios!</p>
    <p>
      <button @click="logout">Cerrar Sesión</button>
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      customer: {}
    };
  },
  methods: {
    async logout() {
      const csrftoken = document.cookie.match(/csrftoken=([^;]*)/)[1];
      try {
        const response = await fetch(`${import.meta.env.VITE_APP_API_URL}/customers/logout/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
          credentials: 'include',
          body: JSON.stringify({})
        });
        console.log(response)
        const data = await response.json();
        if (data.success) {
          this.$router.push('/login');
        } else {
          this.message = data.error;
        }
      } catch (error) {
        this.message = 'Ocurrió un error al cerrar la sesión.';
        console.log(error);
      }
    }
  }
};
</script>
