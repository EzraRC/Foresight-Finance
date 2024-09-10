<template>
    <!--Will edit to make more mobile friendly-->
    <nav class="navbar">
        <div class="FFLogo">
            <router-link to="/">Foresight Finance</router-link>
        </div>
        <ul class="links">
            <li><router-link to="/">Home</router-link></li>
            <li><router-link to="/AIPR">AI Pattern Recognizer</router-link></li>
            <li><router-link to="/GSlearning">Gold Standard Learning</router-link></li>
        </ul>
        <router-link class="login_btn" to="/LoginSignUp">Login</router-link>
        <div class="toggle_btn">
            <i class="fa-solid fa-bars"></i>
        </div>
    </nav>
</template>

<script>

</script>

<style>

li{
  list-style: none;
}

.links{
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
.togggle_btn{
    color: #fff;
    font-size: 1.5rem;
    cursor: pointer;
    display: none;
}

.login_btn {
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

.login_btn:hover {
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
.login_btn.router-link-exact-active{
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

.links a:hover {
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

.FFLogo {
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

.links a.router-link-exact-active {
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