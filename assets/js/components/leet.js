import hljs from 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.5.1/build/es/highlight.min.js'; // TODO: import the needed languages only

const HLJS_ALIASES = {'js':'js','py3':'python'};

Vue.component('leet',{ // TODO(?): move problem & solution to separate components. TBH there is no real need in "leet" being a separate component for now.
	template:`
		<div class="site_block leet">
			<div class="head">
				<h5>Some problems from leetcode. Select problem on the left, click buttons to switch between description & solutions </h5>
			</div>
			<div class="body">
				<div class="problems_list">
					<div class="filters">
						
						<ul class="difficulty_filters">
							<li v-for="(dif,k) in difficulties" :class="['btn',{'active':dif.in_filter}]" @click="toggle_difficulty_filter(dif)">
								{{ k }} <span class="sup">{{ dif.counter }}</span>
							</li>
						</ul>
					</div>
					<ul class="problems_nav">
					<template v-for="(item,index) in problems_data">
						<li v-if="does_pass_filters(item)" :class="[{'active':selected_item==item}]" @click="select_problem(item)">
							{{ item.problem.title }}
						</li>
					</template>
					</ul>
				</div>
				<div class="problem">
				<template v-if="selected_item">
					<ul class="solution_controls">
						<li :class="['btn',{'active': selected_lang == constants.DESC}]" @click="select_lang(constants.DESC)">Description</li>
						<li v-for="lang in langs" :class="['btn',{'active': selected_lang == lang}]" v-if="selected_item.solutions[lang]" @click="select_lang(lang)">{{ lang }}</li>
					</ul>
					<div class="wrapper">
						<div class="desc" v-if="selected_lang == constants.DESC">
							<div class="header">
								<!--span class="problem_id"># {{ selected_item.problem.id }}</span-->
								<span class="title">{{ selected_item.problem.title }}</span>
								<span class="difficulty">[{{ selected_item.problem.difficulty }}]</span>
							</div>
							<div class="text" v-html="selected_item.problem.description">
							</div>
						</div>
						<div v-else class="solution">
							<div v-if="selected_item.comment" class="comment" v-html="selected_item.comment">
							</div>
							<div v-if="selected_item.solutions[selected_lang].comment" class="comment" v-html="selected_item.solutions[selected_lang].comment">
							</div>
							<code v-if="selected_item.solutions[selected_lang].solution" v-html="highlighted_solution_html">
							</code>
						</div>
					</div>
					</template>
					<template v-else>
						Select the problem
					</template>
					
				</div>
			</div>
		</div>
		`,
		props:['problems_data','langs'], //TODO(?): either sanitize HTML here or swith to BBCode
		data: function(instance) {
			return {
				constants:Object.freeze({
					DESC: 'description'
				}),
				selected_item:null,
				selected_lang:null,
				filter:'',
				difficulties:Object.values(instance.problems_data).reduce(function(acc,cur,index,arr){
					if (Object.keys(cur.solutions).length) {
						if (acc[cur.problem.difficulty]){
							acc[cur.problem.difficulty].counter++
						} else {
							acc[cur.problem.difficulty] = {in_filter:false,counter:1} /*? add smth else ?*/
						}
					}
					
					return acc;
				},{}),
			}
		},
		methods:{
			select_problem:function(item) {
				this.selected_item = item;
				this.selected_lang = this.constants.DESC;
			},
			does_pass_filters:function(item){
				let dif_filters = Object.values(this.difficulties).filter(el=>el.in_filter);
				
				if (dif_filters.length > 0) // at least one selected
					if (this.difficulties[item.problem.difficulty].in_filter !== true)
						return false;
				
				if (!Object.keys(item.solutions).length)
					return false;
				
				return true;
			},
			toggle_difficulty_filter(d){
				d.in_filter = !d.in_filter;
			},
			select_lang(str){
				if (this.langs.indexOf(str) === -1)
					this.selected_lang = this.constants.DESC;
				else
					this.selected_lang = str;
			}
		},
		mounted:function(){
			
		},
		computed:{
			highlighted_solution_html:function(){
				if (this.selected_item?.solutions[this.selected_lang]?.solution){
					return hljs.highlight(this.selected_item?.solutions[this.selected_lang]?.solution, {language: HLJS_ALIASES[this.selected_lang]}).value;
				} else {
					return 'No code for highliting';
				}
			}
		}
	}
)