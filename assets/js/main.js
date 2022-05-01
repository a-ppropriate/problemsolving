import 'https://cdn.jsdelivr.net/npm/vue/dist/vue.js';
import './components/problemsolving.js';

document.addEventListener('DOMContentLoaded',function(){
	let promises = [];
	let index = null;
	let constants = null;
	
	/*
	promises.push(
		fetch('/const.json').then(
			response => response.json().then(
				res => index = res
			)
		)
	);*/
	
	Promise.all(promises).then(values => {
		console.log(index);
		let app = new Vue ({
			el:'#app',
			template:'<problemsolving></problemsolving>',
			mounted:function(){
				console.log('app mounted');
			}
		});
	});
	/*
	fetch('/problems/leetcode/index.json').then(response => {
	   let index = response.json();
	   
	   console.log(index);
		console.log(123);
		let app = new Vue ({
			el:'#app',
			template:'<problemsolving></problemsolving>',
			mounted:function(){
				console.log('app mounted');
			}
		});
	})*/
});