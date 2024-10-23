
<template>
    <div class="form-wrapper">
      <h2>Restablecer Contraseña</h2>
      <form @submit.prevent="resetPassword">
        <div>
          <label>Contraseña Provisional</label>
          <input v-model="temporaryPassword" type="password" name="password" required />
        </div>
        <div>
          <label>Nueva Contraseña</label>
          <input v-model="newPassword" type="password" name="new_password" required />
        </div>
        <div>
          <label>Confirmar Nueva Contraseña</label>
          <input v-model="confirmPassword" type="password" name="confirm_password" required />
        </div>
        <button type="submit">Restablecer Contraseña</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        temporaryPassword: '',
        newPassword: '',
        confirmPassword: '',
        message: ''
      };
    },
    methods: {
      async resetPassword() {
        if (this.newPassword !== this.confirmPassword) {
          this.message = 'Las contraseñas no coinciden';
          return;
        }
  
        try {
          const response = await fetch(`${import.meta.env.VITE_APP_API_URL}/customers/change_password/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              password: this.temporaryPassword,
              new_password: this.newPassword,
              confirm_password: this.confirmPassword
            })
          });
          const data = await response.json();
          if (data.success) {
            this.message = 'Contraseña restablecida exitosamente';
            alert('Contraseña restablecida exitosamente.')
            this.$router.push('/login');
          } else {
            this.message = data.error;
          }
        } catch (error) {
          this.message = 'Ocurrió un error al restablecer la contraseña.';
          console.log(error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* Estilos personalizados para mejorar la interfaz */
  </style>
