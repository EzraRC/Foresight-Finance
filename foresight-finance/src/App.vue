<template>
  <nav>
    <router-link id="FFLogo" to="/">Foresight Finance </router-link>
    <router-link to="/">Home</router-link>
    <router-link to="/about">About</router-link>
  </nav>
  <router-view/>
</template>

<style>
html, body{
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}
#app {
  font-family: "Monda", sans-serif;
  
}

nav {
  padding: 30px;
  background-color: #183243;
  position:fixed; 
  width:100vw;
  
}

nav a {
  font-weight: bold;
  color: #e3b130;
  text-decoration: none;
}

#FFLogo{
  font-size: 2vw;
  text-transform: uppercase;
  line-height:1;
  text-align: center;
  background: linear-gradient(90deg, rgba(186,148,62,1) 0%, rgba(236,172,32,1) 20%, rgba(186,148,62,1) 39%, rgba(249,244,180,1) 50%, rgba(186,148,62,1) 60%, rgba(236,172,32,1) 80%, rgba(186,148,62,1) 100%);
  background-clip: text;
  -webkit-text-fill-color: transparent;	
  animation: shine 3s infinite ease-in-out;
  background-size: 200%;
  background-position: left;
}

nav a.router-link-exact-active {
  /*Will have the actice nav bar links be animated gold when active */
  font-size: 2vw;
  text-transform: uppercase;
  line-height:1;
  text-align: center;
  background: linear-gradient(90deg, rgba(186,148,62,1) 0%, rgba(236,172,32,1) 20%, rgba(186,148,62,1) 39%, rgba(249,244,180,1) 50%, rgba(186,148,62,1) 60%, rgba(236,172,32,1) 80%, rgba(186,148,62,1) 100%);
  background-clip: text;
  -webkit-text-fill-color: transparent;	
  animation: shine 3s infinite ease-in-out;
  background-size: 200%;
  background-position: left;
}

@keyframes shine {
  from{background-position: -10%;}
  to{background-position: 110%}
 
}
</style>
