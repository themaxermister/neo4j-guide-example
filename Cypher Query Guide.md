# Using neo4j

## 1. Select query by nodes

### a) Get all nodes

```sql
MATCH (n) RETURN n
```

### b) Get nodes by entity type

``` sql
MATCH (n:<TYPE>) RETURN n
```

### c) Get property 

``` sql
MATCH (n:<TYPE>) RETURN n.<PROPERTY> AS property_name, n.<PROPERTY> as property_name
```

### d) Get nodes by condition

```sql
MATCH (n:<TYPE>) WHERE <CONDITION> RETURN n
```

### e) LIMIT nodes returned

```sql
MATCH (n:<TYPE>) WHERE <CONDITION> RETURN n LIMIT num
```


### f) SKIP nodes returned

```sql
MATCH (n:<TYPE>) WHERE <CONDITION> RETURN n SKIP num (LIMIT num2)
```

### g) ORDER BY nodes returned

```sql
MATCH (n:<TYPE>) WHERE <CONDITION> RETURN n ORDER BY n.<PROPERTY> (DESC/ASC)
``` 

### h) Filter multiple nodes concurrently

```sql
MATCH (n1:<TYPE>), (n2:<TYPE>) RETURN n1, n2
```

## 2. Select query by relationship

### a) Filter by relationship type

```sql
MATCH (n1:<TYPE A>) - [:<RELATION>]-> (n2:<TYPE B>)
WHERE (CONDITION ON n1.<PROPERTY> and n2.<PROPERTY>)
RETURN n1, n2
```
 
### b) Filter by relationship property

```sql
MATCH (n1:<TYPE A>) - [relation:<RELATION>]-> (n2:<TYPE B>)
WHER (CONDITION ON relation.<PROPERTY>)
RETURN n1, n2
```

### c) Filter by relationship property in comparison with a specific entity

 ```sql
 MATCH(n1:<TYPE A> {<PROPERTY>: property_value}) - [:TEAMMATES] -> (n2:TYPE A)
 RETURN n2
 ```

### c) Filter by relationship property in comparison with a specified entity for a specified condition

```sql
 MATCH (n1:<TYPE A> {<PROPERTY>: property_value}) - [:<RELATION A>] -> (n2:TYPE A)
 MATCH(n2) - [r2:<RELATION B>] -> (n3:<TYPE B>)
 WHERE (CONDITION ON r2.<PROPERTY>)
 RETURN n2
```

### d) Filter by total number of records of relationship

```sql
MATCH (n1:<TYPE A>) - [relation:<RELATION>]-> (n2:<TYPE B>)
RETURN n1.<PROPERTY>, COUNT(relation)
```

### e) Filter by average value of property for relationship

```sql
MATCH (n1:<TYPE A>) - [relation:<RELATION>]-> (n2:<TYPE B>)
RETURN n1.<PROPERTY>, AVG(relation.<PROPERTY>) AS p1
ORDER BY p1 (DESC/ASC)
```

## 3. Query nodes by ID

```sql
MATCH(n1:<TYPE>)
WHERE ID(n1) = num
return n1
```

## 4. Creating nodes and relationships

### a) Creating a node (of multiple types)

```sql
CREATE (:<TYPE A>:<TYPE B>:<TYPE C> {<PROPERTY_1>:property_value, <PROPERTY_2>:property_value})
```

```sql
CREATE (n1:<TYPE A>:<TYPE B>:<TYPE C> {<PROPERTY_1>:property_value, <PROPERTY_2>:property_value})
RETURN n1
```

### b) Create relationship between nodes

```sql
CREATE (:<TYPE A>) - [:<RELATION> {<PROPERTY_1>: property_value}] -> (:<TYPE B> {<PROPERTY_2>: property_value})
```

### c) Create relationships between nodes by condition

```sql
MATCH (n1:<TYPE A> {<PROPERTY_1>: property_value}), (n2:<TYPE B> {<PROPERTY_2>: property_value})
CREATE (n1) - [:<RELATION> {<PROPERTY_3>: property_value}] -> n2
```

## 5. Create new properties in a node

```sql
MATCH(n1:<TYPE>)
WHERE ID(n1) = num
SET n1.<PROPERTY> = property_value
return n1
```

## 5. Update existing properties in a node

### a) Update values of property

```sql
MATCH(n1:<TYPE>)
WHERE ID(n1) = num
SET n1.<PROPERTY_1> = property_value, n1.<PROPERTY_2> = property_value
return n1
```

### b) Add additional type to node

```sql
MATCH(n1:<TYPE>)
WHERE ID(n1) = num
SET n1.NEW_TYPE
return n1
```

### c) Update value of property from specific relationship between 2 nodes

```sql
MATCH (n1 {<PROPERTY_1> = property_value}) - [relation:RELATION] -> (n2:<TYPE>)
SET relation.<PROPERTY> = new_value
RETURN n1, n2
```

## 6. Deleting nodes and relationship

Requires to detach the node's relationship before deleting the node

### a) Delete specific node

```sql
MATCH(n1 {<PROPERTY>: property_value})
DETACH DELETE n1
```

### b) Delete relationship for specific node

```sql
MATCH (n1 {<PROPERTY>: property_value}) - [relation:<RELATION>] -> (:<TYPE>)
DELETE relation
``` 

## 7. Deleting properties in nodes and relationsips

### a) Remove property from node
```sql
MATCH (n1 {<PROPERTY>: property_value})
REMOVE n1.<PROPERTY>
RETURN n1
```

### a) Remove type from node
```sql
MATCH (n1 {<PROPERTY>: property_value})
REMOVE n1:<TYPE>
RETURN n1
```