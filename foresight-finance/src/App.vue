<template>
  <nav>
    <div><router-link id="FFLogo" to="/">Foresight Finance</router-link></div>
    <ul class="middle-links">
      <li><router-link to="/">Home</router-link></li>
      <li><router-link to="/AIPR">AI Pattern Recognizer</router-link></li>
      <li><router-link to="/GSlearning">Gold Standard Learning</router-link></li>
    </ul>
    <router-link class="Login" to="/LoginSignUp">Login</router-link>
  </nav>
  <router-view />
</template>

<style>
html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  font-family: "Monda", sans-serif;

}

li{
  list-style: none;
}

.middle-links{
  display: flex;
  gap: 2rem ;
}

nav{
  padding: 25px;
  background-color: #183243;
  position: fixed;
  width: 100%;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-bottom: 2vh;
  height: 90px;
  gap: 10rem;
}

.middle-links {
  display: flex;
  row-gap: 2rem;
}

nav a{
  font-weight: bold;
  color: #fff;
  text-decoration: none;
}

.Login {
  background-color: #e3b130;
  border: none;
  color: black;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 16px;
}

.Login:hover {
  scale: 1.05;
  background-color: #ffc534;
  border: none;
  color: black;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 16px;
}
.Login.router-link-exact-active{
  scale: 1.05;
  color: black;
  background: linear-gradient(90deg, rgba(186, 148, 62, 1) 0%, rgba(236, 172, 32, 1) 20%, rgba(186, 148, 62, 1) 39%, rgba(249, 244, 180, 1) 50%, rgba(186, 148, 62, 1) 60%, rgba(236, 172, 32, 1) 80%, rgba(186, 148, 62, 1) 100%);
  animation: shine 3s infinite ease-in-out;
  background-size: 250%;
  background-position: left;
  border: none;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 16px;
}

.middle-links a:hover {
  font-weight: bold;
  text-decoration: none;
  text-align: center;
  background: linear-gradient(90deg, rgba(186, 148, 62, 1) 0%, rgba(236, 172, 32, 1) 20%, rgba(186, 148, 62, 1) 39%, rgba(249, 244, 180, 1) 50%, rgba(186, 148, 62, 1) 60%, rgba(236, 172, 32, 1) 80%, rgba(186, 148, 62, 1) 100%);
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 3s infinite ease-in-out;
  background-size: 200%;
  background-position: left;
}

#FFLogo {
  font-size: 1.5rem;
  text-transform: uppercase;
  line-height: 1;
  text-align: center;
  background: linear-gradient(90deg, rgba(186, 148, 62, 1) 0%, rgba(236, 172, 32, 1) 20%, rgba(186, 148, 62, 1) 39%, rgba(249, 244, 180, 1) 50%, rgba(186, 148, 62, 1) 60%, rgba(236, 172, 32, 1) 80%, rgba(186, 148, 62, 1) 100%);
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 3s infinite ease-in-out;
  background-size: 200%;
  background-position: left;
  margin: auto 1rem;
}

.middle-links a.router-link-exact-active {
  /*Will have the actice nav bar links be animated gold when active */
  font-size: 1.5vw;
  text-transform: uppercase;
  line-height: 1;
  text-align: center;
  background: linear-gradient(90deg, rgba(186, 148, 62, 1) 0%, rgba(236, 172, 32, 1) 20%, rgba(186, 148, 62, 1) 39%, rgba(249, 244, 180, 1) 50%, rgba(186, 148, 62, 1) 60%, rgba(236, 172, 32, 1) 80%, rgba(186, 148, 62, 1) 100%);
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 3s infinite ease-in-out;
  background-size: 200%;
  background-position: left;
}



@keyframes shine {
  from {
    background-position: -10%;
  }

  to {
    background-position: 110%
  }

}
</style>
