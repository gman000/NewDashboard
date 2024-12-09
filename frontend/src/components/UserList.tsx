import { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, Text, Button, Flex, Box, Container, Heading, Badge } from '@radix-ui/themes';

interface User {
  id: number;
  login_id: string;
  email: string;
  created_time: string;
  country: string;
  user_roles: string;
  last_sync: string;
}

interface PaginatedResponse {
  users: User[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalUsers, setTotalUsers] = useState(0);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);
        const response = await axios.get<PaginatedResponse>(`http://127.0.0.1:5002/api/users?page=${page}&per_page=50`);
        setUsers(response.data.users);
        setTotalPages(response.data.total_pages);
        setTotalUsers(response.data.total);
        setError(null);
      } catch (err) {
        setError('Failed to fetch users');
        console.error('Error fetching users:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [page]);

  if (loading) {
    return (
      <Flex align="center" justify="center" style={{ minHeight: '100vh' }}>
        <Box className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></Box>
      </Flex>
    );
  }

  if (error) {
    return (
      <Flex align="center" justify="center" style={{ minHeight: '100vh' }}>
        <Box>
          <Heading size="4" color="red" mb="2">Error</Heading>
          <Text color="red">{error}</Text>
        </Box>
      </Flex>
    );
  }

  return (
    <Container size="4">
      <Flex justify="between" align="center" mb="6">
        <Box>
          <Heading size="6">User List</Heading>
          <Text color="gray" mt="1">Total Users: {totalUsers}</Text>
        </Box>
        <Text color="gray">Showing {users.length} users per page</Text>
      </Flex>
      
      <Box mb="6">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {users.map((user) => (
            <Card key={user.id} style={{ height: '100%' }}>
              <Flex direction="column" gap="3">
                <Box>
                  <Text as="div" size="2" weight="bold" trim="start">
                    {user.email || 'No Email'}
                  </Text>
                  {user.user_roles && (
                    <Flex gap="1" mt="1" wrap="wrap">
                      {user.user_roles.split(',').map((role, index) => (
                        <Badge key={index} color="blue" variant="soft">
                          {role}
                        </Badge>
                      ))}
                    </Flex>
                  )}
                </Box>

                <Box>
                  <Text as="div" size="2" color="gray">
                    <strong>Login ID:</strong> {user.login_id || 'N/A'}
                  </Text>
                  <Text as="div" size="2" color="gray">
                    <strong>Country:</strong> {user.country || 'N/A'}
                  </Text>
                  {user.created_time && (
                    <Text as="div" size="2" color="gray">
                      <strong>Created:</strong>{' '}
                      {new Date(user.created_time).toLocaleDateString()}
                    </Text>
                  )}
                  {user.last_sync && (
                    <Text as="div" size="2" color="gray">
                      <strong>Last Sync:</strong>{' '}
                      {new Date(user.last_sync).toLocaleDateString()}
                    </Text>
                  )}
                </Box>
              </Flex>
            </Card>
          ))}
        </div>
      </Box>

      <Flex gap="3" justify="center" align="center">
        <Button 
          onClick={() => setPage((p) => Math.max(1, p - 1))}
          disabled={page === 1}
          variant="soft"
        >
          Previous
        </Button>
        <Text>
          Page {page} of {totalPages}
        </Text>
        <Button
          onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
          disabled={page === totalPages}
          variant="soft"
        >
          Next
        </Button>
      </Flex>
    </Container>
  );
}