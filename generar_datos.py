import os
import pandas as pd
from faker import Faker
import random


fake = Faker('es_ES')
Faker.seed(42)  # Para reproducibilidad de los datos

def generar_transacciones(num_registros=1000):
    print(f"Generando {num_registros} transacciones sintéticas...")
    
    categorias = ['Supermercado', 'Tecnología', 'Servicios', 'Ocio', 'Transporte', 'Salud']
    
    registros = []
    for i in range(1, num_registros + 1):
        fecha = fake.date_time_between(start_date='-6m', end_date='now')
        categoria = random.choice(categorias)
        
       
        if categoria == 'Tecnología':
            monto = round(random.uniform(50.0, 1200.0), 2)
        elif categoria == 'Supermercado':
            monto = round(random.uniform(10.0, 150.0), 2)
        else:
            monto = round(random.uniform(5.0, 80.0), 2)
            
        registros.append({
            'id_transaccion': f"TXN-{i:05d}",
            'fecha': fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'cliente': fake.name(),
            'categoria': categoria,
            'monto': monto,
            'metodo_pago': random.choice(['Tarjeta Crédito', 'Tarjeta Débito', 'Transferencia', 'Efectivo'])
        })
        
    df = pd.DataFrame(registros)
    
   
    os.makedirs('data', exist_ok=True)
    archivo_salida = 'data/transacciones_raw.csv'
    df.to_csv(archivo_salida, index=False)
    print(f"¡Datos generados con éxito y guardados en '{archivo_salida}'!")

if __name__ == '__main__':
    generar_transacciones(1500)