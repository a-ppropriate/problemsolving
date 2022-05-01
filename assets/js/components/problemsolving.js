import './leet.js';
const SITES = ['leet'];

const BASE_PATH ='./problems/leetcode/'; //TODO(?): move constants to a separate file to be used by both this and js script
const SUPPORTED_LANGS = ['js','py3'];
const INDEX_FILENAME = 'index.json';

Vue.component('problemsolving',{
	template:`
		<div class="container" v-cloak>
			<div class="controls" v-if="available.length>1">
				Here be controls (if will ever be decided to add more sites than just leetcode).
			</div>
			<div class="wrapper">
				<template v-if="data_loaded">
					<component :is="selected" :problems_data="problems" :langs="SUPPORTED_LANGS"></component>
				</template>
				<template v-else>
					Loading...
				</template>
			</div>
		</div>
		`,
		data: function() {
			return {
				available:SITES,
				selected:SITES[0],
				data_loaded:false,
				problems:null,
				SUPPORTED_LANGS:SUPPORTED_LANGS
			}
		},
		beforeMount:function(){
			fetch(BASE_PATH + INDEX_FILENAME).then(response => response.json().then( val =>{
					this.data_loaded = true;
					this.problems = val;
				}
			))
		},
		mounted:function(){
			
		}
	}
)