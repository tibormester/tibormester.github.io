class Person 

    def initialize(n, a)
        @name = n
        @age = a
    end

    def getAge()
        return @age
    end

    def setAge(x)
        @age = x
    end

    def changeAge(x)
        @age = x
    end

    def getName()
        return @name
    end

end

class Student < Person 
    
    def initialize(n, a, g)
        super(n, a)
        @grade = g
    end

    def getGrade()
        return @grade
    end

    def changeGrade(x)
        @grade = x
    end

end

class Staff < Person 

    def initialize(n, a, p)
        super(n, a)
        @position = p
    end

    def getPosition()
        return @position
    end

    def changePosition(newP)
        @position = newP
    end
end

class Roster 

    def initialize()
        @roster = Array.new
    end

    def add(person)
        @roster.push(person)
    end
    
    def size()
        return @roster.length
    end

    def remove(person)
        @roster.delete(person)
    end

    def getPerson(name)
        for person in @roster do
            if person.getName == name
                return person
            end
        end
        return nil
    end

    def map()
        for person in @roster do
            yield person
        end
        return nil
    end
end
