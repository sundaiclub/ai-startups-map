"use client"
import { Button } from "../components/button"
// import { Input } from "@/components/input"
import React from 'react'
import { ChevronRight, BarChart, Users, Building, CheckCircle } from "lucide-react"
import Link from "next/link"

export default function Component() {
    const openNewTab = () => {
      window.open('https://forms.gle/LNVZ5eF2tUKcinrL8', '_blank');
    };
  
  return (
    <div className="flex flex-col min-h-screen bg-[#f5e6d3]">
      <header className="px-4 lg:px-6 h-14 flex items-center bg-[#e6d2b5]">
        <Link className="flex items-center justify-center" href="#">
          <Building className="h-6 w-6 text-[#8b6e4e]" />
          <span className="sr-only">B2B Connect</span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link className="text-sm font-medium hover:underline underline-offset-4 text-[#5e4a33]" href="#">
            Features
          </Link>
          <Link className="text-sm font-medium hover:underline underline-offset-4 text-[#5e4a33]" href="#">
            Pricing
          </Link>
          <Link className="text-sm font-medium hover:underline underline-offset-4 text-[#5e4a33]" href="#">
            About
          </Link>
          <Link className="text-sm font-medium hover:underline underline-offset-4 text-[#5e4a33]" href="#">
            Contact
          </Link>
        </nav>
      </header>
      <main className="flex-1">
        <section className="w-full flex justify-center py-12 md:py-24 lg:py-32 xl:py-48">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none text-[#5e4a33]">
                  Find Your Perfect B2B Customers
                </h1>
                <p className="mx-auto max-w-[700px] text-[#8b6e4e] md:text-xl">
                  Connect with companies ready to buy your product. Expand your B2B network and boost your sales today.
                </p>
              </div>
              <div className="space-x-4">
                <Button className="inline-flex items-center justify-center bg-[#8b6e4e] text-white hover:bg-[#725a3e]">
                  Get Started
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
                <Button variant="outline" className="text-[#8b6e4e] border-[#8b6e4e] hover:bg-[#e6d2b5]">Learn More</Button>
              </div>
            </div>
          </div>
        </section>
        <section className="w-full py-12 md:py-24 flex justify-center lg:py-32 bg-[#e6d2b5]">
          <div className="container px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl text-center mb-12 text-[#5e4a33]">Why Choose Us?</h2>
            <div className="grid gap-10 sm:grid-cols-2 md:grid-cols-3">
              <div className="flex flex-col items-center space-y-3 text-center">
                <BarChart className="h-12 w-12 text-[#8b6e4e]" />
                <h3 className="text-xl font-bold text-[#5e4a33]">Data-Driven Matching</h3>
                <p className="text-[#8b6e4e]">
                  Our AI algorithms match you with companies most likely to need your product.
                </p>
              </div>
              <div className="flex flex-col items-center space-y-3 text-center">
                <Users className="h-12 w-12 text-[#8b6e4e]" />
                <h3 className="text-xl font-bold text-[#5e4a33]">Extensive Network</h3>
                <p className="text-[#8b6e4e]">
                  Access thousands of potential B2B customers across various industries.
                </p>
              </div>
              <div className="flex flex-col items-center space-y-3 text-center">
                <CheckCircle className="h-12 w-12 text-[#8b6e4e]" />
                <h3 className="text-xl font-bold text-[#5e4a33]">Verified Leads</h3>
                <p className="text-[#8b6e4e]">
                  All potential customers are pre-screened and verified for quality assurance.
                </p>
              </div>
            </div>
          </div>
        </section>
        <section className="w-full py-12 md:py-24 lg:py-32 flex justify-center ">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl text-[#5e4a33]">Ready to Become Part of the Net?</h2>
                <p className="mx-auto max-w-[600px] text-[#8b6e4e] md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Join thousands of successful businesses who have found their ideal B2B customers through our platform.
                </p>
              </div>
              <div className="w-full max-w-sm space-y-2">
                
                
                  <Link href="https://forms.gle/LNVZ5eF2tUKcinrL8" target="_blank">
                    <Button size="lg" className="bg-[#8b6e4e] text-white hover:bg-[#725a3e]" onClick={openNewTab} >Subscribe</Button>
                  </Link>
                
                <p className="text-xs text-[#8b6e4e]">
                  By subscribing, you agree to our Terms & Conditions and Privacy Policy.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
      <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t border-[#8b6e4e] bg-[#e6d2b5]">
        <p className="text-xs text-[#8b6e4e]">© 2023 B2B Connect. All rights reserved.</p>
        <nav className="sm:ml-auto flex gap-4 sm:gap-6">
          <Link className="text-xs hover:underline underline-offset-4 text-[#5e4a33]" href="#">
            Terms of Service
          </Link>
          <Link className="text-xs hover:underline underline-offset-4 text-[#5e4a33]" href="#">
            Privacy
          </Link>
        </nav>
      </footer>
    </div>
  )
}