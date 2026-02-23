import React from 'react';

function Pagination({ pagination, onPageChange }) {
  const { count, next, previous } = pagination;

  const extractPageNumber = (url) => {
    if (!url) return null;
    const match = url.match(/page=(\d+)/);
    return match ? parseInt(match[1]) : null;
  };

  const currentPage = extractPageNumber(previous) ? extractPageNumber(previous) + 1 : 1;
  const totalPages = Math.ceil(count / 10);

  const handlePrev = () => {
    if (previous) {
      onPageChange(previous);
    }
  };

  const handleNext = () => {
    if (next) {
      onPageChange(next);
    }
  };

  return (
    <div className="d-flex justify-content-between align-items-center mt-4">
      <div className="text-muted">
        Всего записей: <strong>{count}</strong>
      </div>
      
      <nav aria-label="Page navigation">
        <ul className="pagination mb-0">
          <li className={`page-item ${!previous ? 'disabled' : ''}`}>
            <button 
              className="page-link" 
              onClick={handlePrev}
              disabled={!previous}
            >
              ← Назад
            </button>
          </li>
          
          <li className="page-item active">
            <span className="page-link">
              Страница {currentPage} из {totalPages}
            </span>
          </li>
          
          <li className={`page-item ${!next ? 'disabled' : ''}`}>
            <button 
              className="page-link" 
              onClick={handleNext}
              disabled={!next}
            >
              Вперед →
            </button>
          </li>
        </ul>
      </nav>
    </div>
  );
}

export default Pagination;