class TextProcessor:
    def __init__(self, chunk_size=2000):
        self.chunk_size = chunk_size
        
    def split_text(self, text):
        """将文本分割成更小的块"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            if current_size + word_size > self.chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
                
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks
