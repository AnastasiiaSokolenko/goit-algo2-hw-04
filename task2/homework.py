from trie import Trie


class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        # ---- Валідація ----
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")

        if pattern == "":
            return 0

        count = 0

        # Обхід усіх слів у Trie
        def dfs(node, path):
            nonlocal count

            if node.value is not None:
                word = "".join(path)
                if word.endswith(pattern):
                    count += 1

            for ch, child in node.children.items():
                path.append(ch)
                dfs(child, path)
                path.pop()

        dfs(self.root, [])
        return count

    def has_prefix(self, prefix) -> bool:
        # ---- Валідація ----
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")

        if prefix == "":
            return False

        current = self.root
        for ch in prefix:
            if ch not in current.children:
                return False
            current = current.children[ch]

        return True


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1      # apple
    assert trie.count_words_with_suffix("ion") == 1    # application
    assert trie.count_words_with_suffix("a") == 1      # banana
    assert trie.count_words_with_suffix("at") == 1     # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") is True
    assert trie.has_prefix("bat") is False
    assert trie.has_prefix("ban") is True
    assert trie.has_prefix("ca") is True
