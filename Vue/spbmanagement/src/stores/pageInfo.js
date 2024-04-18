// 或者使用工厂函数
export function createPageInfo() {
  return {
    currentPage: 1,
    pageCount: 1,
    pagerCount: 5,
    pageSize: 10,
    total: 0
  }
}
