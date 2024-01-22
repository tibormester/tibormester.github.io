class Translator
  
  class Word

    def initialize(n)
      @pos = "null"
      @translations = Hash.new
      @name = n
    end

    def setPOS(p)
      @pos = p
    end

    def getPOS()
      return @pos
    end

    def translate(language)
      return @translations[language]
    end

    def addTranslation(language, translation)
      @translations[language] = translation
    end

    def getName()
      return @name
    end

  end
    
    def initialize(words_file, grammar_file)
      @words = []
      @grammars = {}
      updateLexicon(words_file)
      updateGrammar(grammar_file)
    end

    def getWordIndex(name)
      ans = []
      for i in 0..@words.length-1 do
        if @words[i].getName == name
          ans.push(i)
        end
      end
      if ans.length == 1 
        return ans[0]
      end
      if ans.length == 0 
        return -1
      end
      return ans
    end

    def getWordPOS(language, pos)
      for word in @words do
        if word.getPOS == pos
          if language == "English"
            return word.getName
          else
            if word.translate(language) != nil
              return word.translate(language)
            end
          end
        end
      end
      #returns nil if no words exist with the POS in that language
      return nil
    end

    def getForeignPOS(language, name)
      if language == "English"
        return @words[getWordIndex(name)].getPOS()
      end
      for word in @words do
        if word.translate(language) == name
          return word.getPOS()
        end
      end
      return nil
    end

    #needs a way to differentiate between two words with the same name but different pos
    def translateWord(name, language1, language2)
      if language1 == "English"
        return @words[getWordIndex(name)].translate(language2)
      end
      for word in @words
        if word.translate(language1) == name
          if language2 == "English"
            return word.getName
          end
          return word.translate(language2)
        end
      end
    end
    # part 1
  
    def updateLexicon(inputfile)
      File.readlines(inputfile).each do |line|
        next unless line =~ /([a-z\-]+),\s+([A-Z]{3}),\s+([a-zA-Z0-9\-:,\s]+)/
          #checks that the word doesnt already exist or if so this is a new part of speech
          index = getWordIndex($1)
          #if there is a single instance of the word with the same name
          if index.class == Integer
            #if the word doesnt exist
            if index == -1 
              word = Word.new($1)
            else
              word = @words[index]
              #checks if the existing word has the right POS, if not, creates a new one
              if word.getPOS() != $2
                word = Word.new($1)
              end
            end
          elsif index.class == Array
            #if multiple words of the same name, finds the one with the right POS
            for i in index do
              if @words[i].getPOS() == $2
                word = @words[i]
              end
            end
          end
          word.setPOS($2)
          string = $3
          #when there is a Language:translation, ... string remaining, keeps adding these key value pairs to the hash
          while string =~ /\s*([A-Z][a-z0-9]*):([a-z\-]+),?(.*)/
            string = $3
            word.addTranslation($1.strip, $2.strip)
          end
          #ensures the translations didnt terminate after a malformed pair
          if string =~ /\s*/
            @words.push(word)
          end
        end
      end
    

    def updateGrammar(inputfile)
      File.readlines(inputfile).each do |line|
        next unless line =~ /([A-Z][a-z0-9]*):\s+([A-Z1-9\{\},\s]+)/
          lang = $1
          string = $2
          gram = []
          while string =~ /\s*([A-Z]{3})\{?([1-9])?\}?,?\s*(.*)/
            string = $3
            gram.push($1)
            if $2 != nil
              i = 1
              while i < $2.to_i do
                gram.push($1)
                i += 1
              end
            end
          end
          #checks that the line is not malformed
          if string =~ /^s*$/
            @grammars[lang] = gram
          end
        end
    end 
      
    
    
    # part 2
  
    def generateSentence(language, struct)
      if struct.class == String
        grammar = @grammars[struct]
        if grammar == nil
         return nil
        end
      elsif struct.class == Array
        grammar = struct
      else
        return nil
      end
      string = ""
      if grammar.length < 1
        #return nil #gives an error cant match nill
      end
      for pos in grammar do
        if getWordPOS(language, pos) != nil
          string += getWordPOS(language, pos) + " "
        else
          return nil
        end
      end
      return string.strip
    end
  
    def checkGrammar(sentence, language)
      string = sentence
      i = 0
      if @grammars[language] == nil 
        return false
      end
      if @grammars[language].class != Array
        return false
      end
      while string =~ /\s*([a-z\-]+)\s*(.*)/
        word = $1
        string = $2
        if i >= @grammars[language].length
          return false
        end
        validPOS = false
        if language == "English"
          pos = @words[getWordIndex(word)].getPOS()
          if pos == @grammars[language][i]
            validPOS = true
          end
        else
          for w in @words do
            if w.translate(language) == word
              pos = w.getPOS()
              if pos == @grammars[language][i]
                validPOS = true
              end
            end
          end
        end
        if validPOS == false
          return false
        end
        i = i + 1
      end
      if string =~ /^\s*$/ 
        if i == @grammars[language].length
          return true
        end
      end
      return false 
    end
  
    def changeGrammar(sentence, struct1, struct2)
      if struct1.class == String
        grammar1 = @grammars[struct1]
      else
        grammar1 = struct1
      end
      if struct2.class == String
        grammar2 = @grammars[struct2]
      else
        grammar2 = struct2
      end
      grammarHash = {}
      for pos in grammar1 do
        grammarHash[pos] = Array.new
      end
      string = sentence
      i = 0
      while string =~ /\s*([a-z\-]+)\s*([a-z\-\s]*)/
        word = $1
        string = $2
        grammarHash[grammar1[i]].push(word)
        i = i + 1
      end
      string = ""
      for pos in grammar2 do
        if grammarHash[pos] == nil
          return nil
        end
        word = grammarHash[pos].pop()
        if word == nil
          return nil
        end
        string += word + " "
      end
      return string.strip
    end

    # part 3
  
    def changeLanguage(sentence, language1, language2)
      if checkGrammar(sentence, language1) == false
        return nil
      end
      string = sentence
      newSentence = ""
      while string =~ /\s*([a-z\-]+)\s*([a-z\-\s]*)/
        word = $1
        string = $2
        word = translateWord(word, language1, language2)
        if word == nil
          return nil
        end
        newSentence += word + " "
      end
      return newSentence.strip
    end
  
    def changeLanguageWOGrammar(sentence, language1, language2)
      string = sentence
      newSentence = ""
      while string =~ /\s*([a-z\-]+)\s*([a-z\-\s]*)/
        word = $1
        string = $2
        word = translateWord(word, language1, language2)
        if word == nil
          return nil
        end
        newSentence += word + " "
      end
      return newSentence.strip
    end

    def translate(sentence, language1, language2)
      if checkGrammar(sentence, language1) == false
        return nil
      end
      if @grammars[language1].length != @grammars[language2].length
        return nil
      end
      newSentence = changeGrammar(sentence, language1, language2)
      if newSentence == nil
        return nil
      end
      return changeLanguageWOGrammar(newSentence, language1, language2)
    end
  end  