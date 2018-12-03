import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { InstantSearch, Hits, SearchBox, Highlight, Pagination, Configure } from 'react-instantsearch-dom';
import RepositoryContainer from './RepositoryContainer';

let renderApp = () => {

  function SearchArea() {
    return (
      <div className="mb-4">
        <SearchBox />
      </div>
    )
  }

  function Search() {
    return (
      <div className="mb-4">
        <Hits hitComponent={RepositoryContainer} />
      </div>
    );
  }

  function PoweredByAlgolia() {
    return (
      <div className="row justify-content-end mt-1 mb-5">
        <img src='/static/powered_by_algolia.svg'></img>
      </div>
    )
  }

  function PaginationContainer() {
    return (
      <div className="mb-3">
        <Pagination />
      </div>
    );
  }

  const App = () => (
    <InstantSearch
      appId={algoliaAppId}
      apiKey={algoliaSearchKey}
      indexName={organisation.toLowerCase()}>

      <SearchArea />
      <Search />
      <Configure hitsPerPage={10} />
      <PaginationContainer />

    </InstantSearch>
  );

  ReactDOM.render(<App />, document.querySelector('#app'));
};

// Load google charts
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(renderApp)