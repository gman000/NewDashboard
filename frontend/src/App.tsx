import { Theme } from '@radix-ui/themes'
import '@radix-ui/themes/styles.css'
import { UserList } from './components/UserList'

function App() {
  return (
    <Theme appearance="light" accentColor="blue" radius="medium">
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="container mx-auto px-4 py-4">
            <h1 className="text-2xl font-bold text-gray-900">User Dashboard</h1>
          </div>
        </header>
        <main>
          <UserList />
        </main>
      </div>
    </Theme>
  )
}

export default App