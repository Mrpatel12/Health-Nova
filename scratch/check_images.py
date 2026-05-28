import urllib.request

urls = {
    'Dr. Aarti Sharma': 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?q=80&w=900&auto=format&fit=crop',
    'Dr. Karan Mehta': 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?q=80&w=900&auto=format&fit=crop',
    'Dr. Nisha Kapoor': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=900&auto=format&fit=crop',
    'Dr. Rahul Gupta': 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?q=80&w=900&auto=format&fit=crop',
    'Dr. Priya Nair': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=900&auto=format&fit=crop',
    'Dr. Anil Verma': 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?q=80&w=900&auto=format&fit=crop',
    'Dr. Meenakshi Rao': 'https://images.unsplash.com/photo-1550831107-1553da8c8464?q=80&w=900&auto=format&fit=crop',
    'Dr. Vikram Singh': 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?q=80&w=900&auto=format&fit=crop',
    'Dr. Sneha Patel': 'https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=900&auto=format&fit=crop',
    'Dr. Arjun Desai': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=900&auto=format&fit=crop',
    'Dr. Kavya Iyer': 'https://images.unsplash.com/photo-1527613426441-4da17471b66d?q=80&w=900&auto=format&fit=crop',
    'Dr. Sameer Joshi': 'https://images.unsplash.com/photo-1614608682850-e0d6ed316d47?q=80&w=900&auto=format&fit=crop',
    'Dr. Ritu Malhotra': 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=900&auto=format&fit=crop',
    'Dr. Sunil Chawla': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=900&auto=format&fit=crop',
}

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"{name}: HTTP {response.status}")
    except Exception as e:
        print(f"{name}: Error {e}")
