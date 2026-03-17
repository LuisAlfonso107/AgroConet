import { ref, onMounted, onUnmounted } from 'vue'

export function useNavbar() {
  const isMobileMenuOpen = ref(false)
  const scrolled = ref(false)

  const toggleMobileMenu = () => {
    isMobileMenuOpen.value = !isMobileMenuOpen.value
  }

  const closeMobileMenu = () => {
    isMobileMenuOpen.value = false
  }

  const handleScroll = () => {
    scrolled.value = window.scrollY > 20
  }

  const handleClickOutside = (event: MouseEvent) => {
    const target = event.target as HTMLElement
    if (isMobileMenuOpen.value && !target.closest('header')) {
      closeMobileMenu()
    }
  }

  onMounted(() => {
    window.addEventListener('scroll', handleScroll)
    document.addEventListener('click', handleClickOutside)
    handleScroll()
  })

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
    document.removeEventListener('click', handleClickOutside)
  })

  return {
    isMobileMenuOpen,
    scrolled,
    toggleMobileMenu,
    closeMobileMenu
  }
}
