<template>
  <div class="big-icons">
    <!-- Search content -->
    <div id="search">
      <i class="fa fa-search"></i><input @keyup="searchEntries()" type="text" name="search" id="search-icon" size="15"
        placeholder="Search content" />
    </div>
    <h1 id="welcome">Welcome to e-Market</h1>
    <!-- Sort content -->
    <div class="dropdown" id="sort-div">
      <i class="fa fa-sort"></i>
      <button class="dropbtn">Sort content
        <i class="fa fa-caret-down"></i>
      </button>
      <div class="dropdown-content">
        <a href="/sort/?sort_key=deals">Deals</a>
        <a href="/sort/?sort_key=name_asc"><i class="fa fa-sort-alpha-asc"></i>Alpahbetical order</a>
        <a href="/sort/?sort_key=name_desc"><i class="fa fa-sort-alpha-desc"></i>Alpahbetical order</a>
        <a href="/sort/?sort_key=numeric_desc"><i class="fa fa-sort-numeric-desc"></i>Price:High-Low</a>
        <a href="/sort/?sort_key=numeric_asc"><i class="fa fa-sort-numeric-asc"></i>Price:Low-High</a>
      </div>
    </div>
    <!-- Sub content Icons-->
    <div id="icons" class="icons">
      <div class="icon-div"><a href="/map"><i class="fa fa-map-marker"></i><span class="icon-text">Maps</span></a></div>
      <div class="icon-div"><a href="/game"><i class="fa fa-gamepad"></i><span class="icon-text">Games</span></a></div>
      <div class="icon-div"><a href="javascript:void(0)"><i class="fa fa-gift"></i><span class="icon-text">Gift</span></a>
      </div>
      <div class="icon-div"><a href="javascript:void(0)"><i class="fa fa-car"></i><span
            class="icon-text">Automobile</span></a></div>
      <div class=" icon-div"><a href=" javascript:void(0)"><i class="fa fa-bed"></i><span
            class="icon-text">Hotels</span></a></div>
      <div class="icon-div"><a href="/news"><i class="fa fa-newspaper-o"></i><span class="icon-text">News</span></a></div>
    </div>

  </div>
</template>


<script>

import { filterEntries } from '@/helpers/script';


export default {
  name: 'BigIcons',
  methods: {
    searchEntries(){
      filterEntries();
    }
  },

}
</script>

