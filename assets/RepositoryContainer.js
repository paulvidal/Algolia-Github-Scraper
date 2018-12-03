import React, { Component } from 'react';
import { Highlight } from 'react-instantsearch-dom';

class RepositoryContainer extends Component {

   constructor(props) {
     super(props);

     this.repositoryName = this.props.hit.repository;
     this.id = 'repo-' + this.repositoryName
     this.contributorCount = 0

     this.repositoryStats = data[this.repositoryName].map((d) => {
       let contributors = Number(d['number_of_new_contributors'])
       this.contributorCount += contributors;
       return [new Date(d['date']), contributors];
     })

     // Add column names
     this.repositoryStats.unshift(['Date', 'New contributors']);

     // Bind method to object
     this.drawChart = this.drawChart.bind(this);
   }

   componentDidMount() {
      this.drawChart();
   }

   drawChart() {
     let options = {
       legend: {position: 'bottom'},
       chartArea: {
         height: '80%',
         width: '90%',
         top: 10,
       },
       width: '100%',
       height: 400,
       hAxis: {
         format: 'MMM yy',
         gridlines: {
           count: 5
         }
       },
       vAxis: {
         format: '#',
         gridlines: {
           count: 5
         }
       }
     };

     let chart = new google.visualization.ColumnChart(document.getElementById(this.id));
     chart.draw(google.visualization.arrayToDataTable(this.repositoryStats), options);
   };

   render() {
     return (
       <div className="row col-12 mt-1">
         <span className="col-12 hit-name">
           <Highlight attribute="repository" hit={this.props.hit} />
         </span>
         <div className="col-12 mt-2">Total contributors count: {this.contributorCount}</div>
         <div className="col-12 mt-4" id={this.id}></div>
       </div>
     )
   }
}

export default RepositoryContainer;