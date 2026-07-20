import { useQuery } from '@tanstack/react-query'
import { getActivities, getCenters, getChild, getRecords } from '../api/mock'

export const useChild = () => useQuery({ queryKey: ['child'], queryFn: getChild })
export const useRecords = () => useQuery({ queryKey: ['records'], queryFn: getRecords })
export const useActivities = () => useQuery({ queryKey: ['activities'], queryFn: getActivities })
export const useCenters = () => useQuery({ queryKey: ['centers'], queryFn: getCenters })
