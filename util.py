
class Util:
    slur_words = set()
    n_words = {"nigga", "nigger", "neger", "nega", "ngr", "negah", "nga", "niga", "niger", "negre","niggr"}
    n_words_contains = {"nigga","nigger","neger","negah","negre","niggr"}
    @classmethod
    def load_slurs_from_file(cls, file_path):
        try:
            with open(file_path, "r") as file:
                cls.slur_words = {line.strip().lower() for line in file if line.strip()}
            print(f"Loaded blacklist with {len(cls.slur_words)} words")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except Exception as e:
            print(f"Error loading slur words: {e}")
    @staticmethod
    def countNWord(message):
        count = 0
        for word in message.split(" "):
            # check with set
            if word in Util.n_words:
                count = 1
                break
            # check n word with a trailing s
            for match in Util.n_words:
                if word.lower() == match.lower()+"s":
                    count = 1
                    break
        for word in Util.n_words_contains:
            if word.lower() in message.lower():
                count = 1
                break
        return count
    @staticmethod
    def countSlurs(message):
        count = 0
        for word in message.split(" "):
            if word.lower() in Util.slur_words:
                count += 1
        return count