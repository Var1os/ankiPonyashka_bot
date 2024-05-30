
class Product:
    def __init__(self, hectar:float, productivity:int, year_coff:list):
        self.hectare = hectar
        self.productivity = productivity
        self.year_coff = year_coff
    
    def Count_year(self, count_year:int) -> list:
        # Массив для возвращения
        massive_productivity = []
        for index in range(0, count_year):
            # Урожайность с гектара умноженная на площать, так же в гектарах
            product = round(self.productivity * self.hectare, 2)
            print(f"Год {index+1}: Гектар = {self.hectare}, Урожайность с полей = {product*100} Кг")

            # Добавление результата в массив, для возврата
            massive_productivity.append(product)
            # Умножение на коэффициенты
            self.hectare = round(self.hectare * self.year_coff[0], 2)
            self.productivity = round(self.productivity * self.year_coff[1], 2)
        
        return massive_productivity

farm = Product(hectar=100, productivity=20, year_coff=[1.05, 1.02])
print(farm.Count_year(6))

