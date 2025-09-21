module.exports = {
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/tests/js'],
  transform: { '^.+\\.js$': 'babel-jest' },
  setupFilesAfterEnv: ['<rootDir>/tests/js/setupJest.js'],
};
