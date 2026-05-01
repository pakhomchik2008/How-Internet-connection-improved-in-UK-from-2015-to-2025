class Member:
    def __init__(self, name, age, interests):
        self.name = name
        self.age = age
        self.interests = interests
        self.friends = {}

    def add_friend(self, friend, weight):  # weighted graph
        if friend not in self.friends:
            self.friends[friend] = weight

    def remove_friend(self, friend):
        if friend in self.friends:
            del self.friends[friend]

    def __repr__(self):
        return f"{self.name} {self.age} {self.interests}"


class Graph:
    def __init__(self):
        # Dictionary to store the members by their names.
        self.members = {}  # nodes

    def add_member(self, m):  # m is object

        if m not in self.members:
            self.members[m.name] = m
            print(f"Member {m} added to the network.")
        else:
            print(f"Member {m} already exists in the network")

    def remove_member(self, m):
        if m.name not in self.members:
            print(f"Member {m} does not exist in the network.")
        else:
            del self.members[m.name]
            print(f"Member {m} has been removed from the network.")

    def add_relationship(self, member1, member2, weight=1):  # member1 and member2 are names

        if member1 not in self.members or member2 not in self.members:
            print(f"One or both members '{member1}', '{member2}' do not exist.")
            return -1
        else:
            member1 = self.members[member1]
            member2 = self.members[member2]

            member1.add_friend(member2.name, weight)
            member2.add_friend(member1.name, weight)  ## remove this line to make it a directional graph

            print(f"Relationship (weight {weight}) added between '{member1}' and '{member2}'.")

    def remove_relationship(self, member1, member2):
        if member1 not in self.members or member2 not in self.members:
            print(f"One or both members '{member1}', '{member2}' do not exist.")
            return -1
        else:
            member1 = self.members[member1]
            member2 = self.members[member2]
            member1.remove_friend(member2.name)
            member2.remove_friend(member1.name)
            print(f"Relationship removed between '{member1}' and '{member2}'.")

    def find_friends(self, member_name):  # finding direct friends
        if member_name in self.members:
            return self.members[member_name].friends
        else:
            print(f"Member '{member_name}' does not exist.")
            return []

    def find_mutual_friends(self, member1, member2):

        friends1 = set(self.find_friends(member1) or [])
        friends2 = set(self.find_friends(member2) or [])
        mutual_friends = friends1.intersection(friends2)
        print(f"{mutual_friends} are mutual between {member1} and {member2}")
        return list(mutual_friends)

    def most_connected_member(self):

        # for x in self.members:
        #   degree= len(self.members[x].friends)
        #  print(f"{self.members[x]} has {degree} friends")
        most_connected_member = max(self.members,
                                    key=len)  # store the element from self.members with the greatest length.
        print(
            f"Most connected member: {most_connected_member} with {len(self.members[most_connected_member].friends)} friends")

    def find_path(self, member1, member2):

        if member1 not in self.members or member2 not in self.members:
            print(f"One or both members '{member1}', '{member2}' do not exist.")
            return -1

        # BFS to find the shortest path
        from collections import deque
        queue = deque([(member1, 0)])
        visited = set()

        while queue:
            current_member, distance = queue.popleft()

            if current_member == member2:
                return distance

            visited.add(current_member)

            for friend in self.members[current_member].friends:
                if friend not in visited:
                    queue.append((friend, distance + 1))

        print(f"No path found between '{member1}' and '{member2}'.")
        return -1

    def degree_of_separation(self, member1, member2):
        # check if both members exist
        if member1 not in self.members or member2 not in self.members:
            print(f"One or both members '{member1}', '{member2}' do not exist.")
            return -1

        # Use the find_path method to compute the path length (degree of separation)
        degree = self.find_path(member1, member2)

        if degree == -1:
            print(f"No path found between '{member1}' and '{member2}'.")
        else:
            print(f"The degree of separation between '{member1}' and '{member2}' is {degree}.")
        return degree

    def get_members(self):
        return list(self.members.keys())

    def get_relationships(self, member_name):

        if member_name in self.members:
            return self.members[member_name].friends
        else:
            print(f"Member '{member_name}' does not exist.")
            return []

    def display_network(self):
        print("Social Network:")
        for member in self.members.values():
            connections = ", ".join([f"{friend} (weight: {weight})" for friend, weight in member.friends.items()])
            print(f"{member}: is connected to {connections}")

    def connected_components(self):
        visited = set()
        components = []

        def dfs(node, component):
            stack = [node]
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    component.append(current)
                    stack.extend(self.members[current].friends.keys())  # Add neighbors to stack

        for member in self.members:
            if member not in visited:
                component = []
                dfs(member, component)
                components.append(component)

        print(f"Connected Components: {components}")
        return components


network = Graph()

m1 = Member("A", 32, "Book Reading")  # Add some members to the network
m2 = Member("B", age=30, interests="Book Reading")
m3 = Member("C", age=30, interests="Book Reading")
m4 = Member("D", age=31, interests="Book Reading")
m5 = Member("E", age=29, interests="Book Reading")
m6 = Member("H", 38, interests="Book Reading")
network.add_member(m1)
network.add_member(m2)
network.add_member(m3)
network.add_member(m4)
network.add_member(m5)
network.add_member(m6)
network.remove_member(m6)
network.connected_components()
# Add some relationships between members
network.add_relationship("A", "B", 1)
network.add_relationship("B", "C", 2)
network.add_relationship("C", "D", 1)
network.add_relationship("C", "A", 1)
network.add_relationship("A", "B", 1)
# network.connected_components()
network.find_mutual_friends("A", "C")
network.most_connected_member()
network.connected_components()
# Find all the friends of Alice
a_friends = network.find_friends("A")
print("\nA's Friends:")
print(a_friends)
print("\nB's Friends:", network.find_friends("B"))
# Find the path between Alice and David
path_length = network.find_path("A", "D")
network.degree_of_separation("A", "D")
print("\nPath Length between A and D:")
print(path_length)

print("\nComplete Social Network:")
network.display_network()
