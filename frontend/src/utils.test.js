import { describe, expect, it } from 'vitest'
import { errorMessage } from './api.js'
import { formatDuration, hhmm, homePathFor, percent, routeColor, ROUTE_COLORS } from './utils.js'

describe('utils', () => {
  it('formatea horas HH:MM', () => {
    expect(hhmm('09:30:00')).toBe('09:30')
    expect(hhmm(null)).toBe('')
  })

  it('formatea duraciones', () => {
    expect(formatDuration(45)).toBe('45 min')
    expect(formatDuration(125)).toBe('2 h 05 min')
  })

  it('asigna colores de ruta de forma cíclica', () => {
    expect(routeColor(0)).toBe(ROUTE_COLORS[0])
    expect(routeColor(ROUTE_COLORS.length)).toBe(ROUTE_COLORS[0])
  })

  it('calcula porcentajes sin dividir por cero', () => {
    expect(percent(50, 200)).toBe(25)
    expect(percent(1, 0)).toBe(0)
  })

  it('redirige a cada rol a su pantalla inicial', () => {
    expect(homePathFor('admin')).toBe('/vehiculos')
    expect(homePathFor('dispatcher')).toBe('/rutas')
    expect(homePathFor('driver')).toBe('/mis-rutas')
  })
})

describe('errorMessage', () => {
  it('usa el detalle de texto de la API', () => {
    expect(errorMessage({ detail: 'Pedido no encontrado' }, 'x')).toBe('Pedido no encontrado')
  })

  it('aplana los errores de validación', () => {
    const body = { detail: [{ loc: ['body', 'capacity_kg'], msg: 'Input should be greater than 0' }] }
    expect(errorMessage(body, 'x')).toBe('capacity_kg: Input should be greater than 0')
  })

  it('usa el texto por defecto si no hay detalle', () => {
    expect(errorMessage(null, 'Error 500')).toBe('Error 500')
  })
})
