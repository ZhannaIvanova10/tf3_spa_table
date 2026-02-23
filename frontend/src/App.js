import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import FilterControls from './components/FilterControls';
import DataTable from './components/DataTable';
import Pagination from './components/Pagination';

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({
    count: 0,
    next: null,
    previous: null
  });
  const [filters, setFilters] = useState({
    column: 'title',
    condition: 'icontains',
    value: ''
  });
  const [sortConfig, setSortConfig] = useState({
    field: null,
    direction: 'asc'
  });

  const fetchData = async (url = '/api/items/') => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      
      // Добавляем фильтры
      if (filters.value) {
        if (filters.column === 'title') {
          params.append('title', filters.value);
        } else {
          const lookup = filters.condition === 'exact' ? '' : `__${filters.condition}`;
          params.append(`${filters.column}${lookup}`, filters.value);
        }
      }
      
      // Добавляем сортировку (кроме даты)
      if (sortConfig.field && sortConfig.field !== 'date') {
        const order = sortConfig.direction === 'desc' ? '-' : '';
        params.append('ordering', `${order}${sortConfig.field}`);
      }
      
      const response = await axios.get(url, { params });
      
      setData(response.data.results);
      setPagination({
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous
      });
    } catch (error) {
      console.error('Ошибка загрузки:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [sortConfig]);

  const handleFilter = () => {
    fetchData();
  };

  const handleSort = (field) => {
    if (field === 'date') return; // Дату не сортируем
    
    setSortConfig(prev => ({
      field,
      direction: prev.field === field && prev.direction === 'asc' ? 'desc' : 'asc'
    }));
  };

  const handlePageChange = (url) => {
    if (url) {
      fetchData(url);
    }
  };

  return (
    <div className="container mt-4">
      <h1 className="mb-4 text-center">Управление таблицей</h1>
      
      <FilterControls 
        filters={filters}
        setFilters={setFilters}
        onFilter={handleFilter}
      />
      
      {loading ? (
        <div className="text-center my-5">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Загрузка...</span>
          </div>
        </div>
      ) : (
        <>
          <DataTable 
            data={data} 
            onSort={handleSort}
            sortConfig={sortConfig}
          />
          
          <Pagination 
            pagination={pagination}
            onPageChange={handlePageChange}
          />
        </>
      )}
    </div>
  );
}

export default App;