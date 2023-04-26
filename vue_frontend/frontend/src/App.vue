
<template>
  <header>
    <nav>
      <ul v-if="userinfo">
        <li><router-link to="/"><i class="fa fa-fw fa-home"></i>Home</router-link></li>
        <li v-show="admin"><router-link to="/about"><i class="fa fa-lock"></i>Admin module</router-link></li>
        <li><router-link to="/admin">Signed in as {{ userinfo.sub }}</router-link></li>
        <li><router-link to="/logout"><i class="fa fa-sign-out"></i>Logout</router-link></li>
        <li><router-link to="/basket"><i class="fa fa-shopping-cart" style="font-size: 25px"></i><span id="items">0</span></router-link></li>
      </ul>
      <ul v-else>
        <li><router-link to="/"><i class="fa fa-fw fa-home"></i>Home</router-link></li>
        <li><router-link to="/login"><i class="fa fa-sign-in"></i>Login</router-link></li>
        <li><router-link to="/basket"><i class="fa fa-shopping-cart" style="font-size: 25px;color: white;"></i><span id="items">0</span></router-link></li>
      </ul>
    </nav>
  </header>
  <router-view />
</template>

